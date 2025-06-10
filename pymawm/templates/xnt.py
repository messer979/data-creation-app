import arrow

tranlog_summary_request_template = {
    "map": {
        "SearchCriteria": [
            {
                "Parameter": "msg_submission_time",
                "Condition": "TimeInterval",
                "Values": [
                    f"gte:{arrow.now().shift(hours=-12)}",
                    f"lte:{arrow.now()}"
                ]
            }
        ],
        "Size": 20,
        "DisplayContent": True
    }
}