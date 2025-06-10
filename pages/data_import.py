"""
Data Import Page
Provides UI for importing data including active inventory transfer functionality
"""

import streamlit as st
import threading
import time
from datetime import datetime
import sys
import os
from components.sidebar import render_sidebar


# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Production imports (commented out for testing)
# from inventory_transfer import run_inventory_transfer, InventoryTransferLogger

# Test imports
from test_inventory_transfer import TestActiveInventoryTransfer, TestInventoryTransferLogger, TransferConfig
from components.app_components import render_sidebar

st.set_page_config(page_title="Data Import", page_icon="📥")
st.title("📥 Data Import")

render_sidebar()

st.markdown("Import and transfer data between environments")

# Create tabs for different import types
tab1, tab2 = st.tabs(["🔄 Active Inventory Transfer", "📊 Bulk Data Import"])

with tab1:
    st.header("🔄 Active Inventory Transfer")
    st.markdown("""
    Transfer active inventory between Manhattan Active WM environments.
    This tool will:
    1. Download inventory data from source environment
    2. Transfer and sync items to target environment  
    3. Upload inventory adjustments to target environment    """)
    
    # Initialize session state for logging (must be outside form)
    if 'transfer_logger' not in st.session_state:
        st.session_state.transfer_logger = None
    if 'transfer_running' not in st.session_state:
        st.session_state.transfer_running = False
    if 'transfer_thread' not in st.session_state:
        st.session_state.transfer_thread = None
    if 'test_mode' not in st.session_state:
        st.session_state.test_mode = False
      # Configuration form
    with st.form("inventory_config"):
        st.subheader("📋 Configuration")
        
        # Test mode toggle
        test_mode = st.checkbox("🧪 Test Mode (Use Dummy Server)", value=False, 
                               help="Use dummy server for testing UI without real API calls")
        
        if test_mode:
            st.info("🧪 **Test Mode Enabled** - Using dummy server at http://localhost:5000")
            st.markdown("Make sure to start the dummy server first: `python dummy_server.py`")
            
            # Check if dummy server is running
            try:
                import requests
                response = requests.get("http://localhost:5000/health", timeout=2)
                if response.status_code == 200:
                    st.success("✅ Dummy server is running and ready!")
                else:
                    st.warning("⚠️ Dummy server responded but may have issues")
            except:
                st.error("❌ Cannot connect to dummy server. Please start it first with: `python dummy_server.py`")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Source Environment**")
            if test_mode:
                from_env = st.text_input("From Environment", value="http://localhost:5000", disabled=True, help="Dummy server URL")
                from_org = st.text_input("From Organization", value="TEST_ORG", help="Test organization")
                from_facility = st.text_input("From Facility", value="TEST_DC", help="Test facility")
                from_token = st.text_input("From Token", value="dummy_token", type="password", help="Test token")
            else:
                from_env = st.text_input("From Environment", placeholder="dev01", help="Source environment (e.g., dev01, test02)")
                from_org = st.text_input("From Organization", placeholder="MANH", help="Source organization code")
                from_facility = st.text_input("From Facility", placeholder="DC01", help="Source facility code")
                from_token = st.text_input("From Token", type="password", help="Source environment API token")
        
        with col2:
            st.markdown("**Target Environment**")
            if test_mode:
                to_env = st.text_input("To Environment", value="http://localhost:5000", disabled=True, help="Dummy server URL")
                to_org = st.text_input("To Organization", value="TEST_ORG", help="Test organization")
                to_facility = st.text_input("To Facility", value="TEST_DC", help="Test facility")
                to_token = st.text_input("To Token", value="dummy_token", type="password", help="Test token")
            else:
                to_env = st.text_input("To Environment", placeholder="test01", help="Target environment (e.g., test01, dev02)")
                to_org = st.text_input("To Organization", placeholder="MANH", help="Target organization code")
                to_facility = st.text_input("To Facility", placeholder="DC01", help="Target facility code")
                to_token = st.text_input("To Token", type="password", help="Target environment API token")
        
        st.markdown("**Transfer Settings**")
        col3, col4, col5 = st.columns(3)
        
        with col3:
            if test_mode:
                zone = st.selectbox("Zone", ["ZONE1", "ZONE2", "ZONE3", "STAGING"], help="Test zone to transfer")
                # Also show target zone for test mode
                target_zone = st.selectbox("Target Zone", ["ZONE1", "ZONE2", "ZONE3", "STAGING"], index=3, help="Target zone for transfer")
            else:
                zone = st.text_input("Zone", placeholder="PICK", help="Zone to transfer inventory for")
        
        with col4:
            download_batch_size = st.number_input("Download Batch Size", min_value=1, max_value=1000, value=200 if not test_mode else 50, help="Records per download batch")        
        with col5:
            upload_batch_size = st.number_input("Upload Batch Size", min_value=1, max_value=100, value=50 if not test_mode else 25, help="Records per upload batch")        

        # Submit button
        if st.form_submit_button("🚀 Start Transfer", type="primary", use_container_width=True):
            st.session_state.submitted = True
    
    # Handle form submission
    if st.session_state.get('submitted', False):
        # Validate required fields
        required_fields = {
            'From Environment': from_env,
            'From Organization': from_org,
            'From Facility': from_facility,
            'From Token': from_token,
            'To Environment': to_env,
            'To Organization': to_org,
            'To Facility': to_facility,
            'To Token': to_token,
            'Zone': zone
        }
        missing_fields = [name for name, value in required_fields.items() if not value]
        
        if missing_fields:
            st.error(f"❌ Please fill in all required fields: {', '.join(missing_fields)}")
        else:
            # Store test mode in session state
            st.session_state.test_mode = test_mode
            
            if test_mode:
                # Create test configuration
                config = TransferConfig(
                    source_url="http://localhost:5000",
                    target_url="http://localhost:5000",
                    source_zones=[zone],
                    target_zone=target_zone if 'target_zone' in locals() else "STAGING",
                    page_size=download_batch_size,
                    max_pages=10  # Limit for testing
                )
                print('iunitialized')
                # Initialize test logger and start transfer
                st.session_state.transfer_logger = TestInventoryTransferLogger()
                st.session_state.transfer_running = True
                
                def run_test_transfer():
                    """Run the test transfer in a separate thread"""
                    try:
                        test_transfer = TestActiveInventoryTransfer(st.session_state.transfer_logger)
                        success = test_transfer.transfer_inventory(config)
                        print(success)

                        if success:
                            st.session_state.transfer_logger.success("🎉 Test transfer completed successfully!")
                        else:
                            st.session_state.transfer_logger.error("❌ Test transfer completed with errors")
                    except Exception as e:
                        try:
                            st.session_state.transfer_logger.error(f"❌ Test transfer failed: {str(e)}")
                        except Exception:
                            raise
                    finally:
                        st.session_state.transfer_running = False
                  # Start test transfer in background thread
                st.session_state.transfer_thread = threading.Thread(target=run_test_transfer)
                st.session_state.transfer_thread.start()
            else:
                # Production mode - commented out for testing
                st.error("🚫 Production mode is disabled for testing. Please use Test Mode.")
                st.info("To enable production mode, uncomment the production imports and code sections.")
                
                # PRODUCTION CODE (commented out for testing):
                """
                # Create production configuration
                config = {
                    'zone': zone,
                    'download_batch_size': download_batch_size,
                    'upload_batch_size': upload_batch_size,
                    'from_env': from_env,
                    'from_org': from_org,
                    'from_facility': from_facility,
                    'from_token': from_token,
                    'to_env': to_env,
                    'to_org': to_org,
                    'to_facility': to_facility,
                    'to_token': to_token
                }
                
                # Initialize logger and start transfer
                st.session_state.transfer_logger = InventoryTransferLogger()
                st.session_state.transfer_running = True
                
                def run_transfer():
                    # Run the transfer in a separate thread
                    try:
                        success = run_inventory_transfer(config, st.session_state.transfer_logger)
                        if success:
                            st.session_state.transfer_logger.success("🎉 Transfer completed successfully!")
                        else:
                            st.session_state.transfer_logger.error("❌ Transfer completed with errors")
                    except Exception as e:
                        st.session_state.transfer_logger.error(f"❌ Transfer failed: {str(e)}")
                    finally:
                        st.session_state.transfer_running = False
                
                # Start transfer in background thread
                st.session_state.transfer_thread = threading.Thread(target=run_transfer)
                st.session_state.transfer_thread.start()
                """
            
            st.success("✅ Transfer started! Monitor progress below.")
            st.rerun()
    
    # Display transfer status and logs
    if st.session_state.transfer_logger:
        st.markdown("---")
        st.subheader("📊 Transfer Status")
        
        # Status indicator
        if st.session_state.transfer_running:
            st.info("🔄 Transfer in progress...")
            # Auto-refresh every 2 seconds while running
            time.sleep(2)
            st.rerun()
        else:
            st.success("✅ Transfer completed")
        
        # Log display
        logs = st.session_state.transfer_logger.get_logs()
        
        if logs:
            st.subheader("📋 Transfer Log")
            
            # Log filtering
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                show_all = st.checkbox("Show all log levels", value=True)
            with col2:
                if st.button("🔄 Refresh Logs"):
                    st.rerun()
            with col3:
                if st.button("🗑️ Clear Logs"):
                    st.session_state.transfer_logger.clear()
                    st.rerun()
            
            # Create log container
            log_container = st.container()
            
            with log_container:
                # Display logs in reverse order (newest first)
                for log_entry in reversed(logs[-50:]):  # Show last 50 logs
                    level = log_entry['level']
                    timestamp = log_entry['timestamp']
                    message = log_entry['message']
                    step = log_entry.get('step', '')
                    
                    # Skip non-essential logs if not showing all
                    if not show_all and level not in ['ERROR', 'SUCCESS', 'STEP']:
                        continue
                    
                    # Style based on log level
                    if level == 'ERROR':
                        st.error(f"🔴 {timestamp} | {message}")
                    elif level == 'SUCCESS':
                        st.success(f"🟢 {timestamp} | {message}")
                    elif level == 'WARNING':
                        st.warning(f"🟡 {timestamp} | {message}")
                    elif level == 'STEP':
                        st.info(f"📍 {timestamp} | {message}")
                    else:
                        st.text(f"ℹ️ {timestamp} | {message}")
            
            # Download logs button
            if logs:
                log_text = "\n".join([f"{log['timestamp']} | {log['level']} | {log['message']}" for log in logs])
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.download_button(
                    label="📥 Download Transfer Log",
                    data=log_text,
                    file_name=f"inventory_transfer_log_{timestamp}.txt",
                    mime="text/plain",
                    help="Download the complete transfer log"
                )

with tab2:
    st.header("📊 Bulk Data Import")
    st.markdown("*Coming soon - Additional bulk data import functionality*")
    
    st.info("This section will contain additional data import tools such as:")
    st.markdown("""
    - CSV file imports
    - JSON template imports
    - Database migrations
    - API data synchronization
    """)
    
    # Placeholder for future functionality
    uploaded_file = st.file_uploader("Choose a file to import", type=['csv', 'json', 'xlsx'])
    if uploaded_file:
        st.info("File upload functionality will be implemented here")

# Add helpful information in sidebar
with st.sidebar:
    st.markdown("### 💡 Help & Tips")
    
    with st.expander("🔧 Environment Setup"):
        st.markdown("""
        **Environment Format**: Use short names like:
        - `dev01`, `test02`, `stage01`
        - Do not include full URLs
        
        **Tokens**: Use valid API tokens for each environment
        """)
    
    with st.expander("⚠️ Important Notes"):
        st.markdown("""
        - Cannot transfer TO production environments
        - Large transfers may take significant time
        - Monitor the log for progress and errors
        - Failed records are saved to 'Failed/' directory
        """)
    
    with st.expander("📊 Batch Size Guidelines"):
        st.markdown("""
        **Download Batch Size**: 
        - Recommended: 100-500
        - Higher = faster but more memory usage
        
        **Upload Batch Size**: 
        - Recommended: 25-100  
        - Lower = more reliable for large datasets
        """)