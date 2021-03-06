import sachima.handler as han
from sachima.model import Data
from sachima.log import logger


def run(user_params, api_params):
    """
    run main defined by user see example
    user_params: dict
    api_params: dict
    return: json str
    """

    logger.info("api_params: " + str(api_params))
    logger.info("user_params: " + str(user_params["params"]))
    # combine two dict  api_params will overwrite user_params
    params = {**user_params["params"], **api_params}
    logger.info("combined params: " + str(params))

    if "model" in user_params and user_params["model"]:
        data_in = [
            Data(dataname, source, params).data
            for dataname, source in user_params["model"]
        ]
    else:
        data_in = None

    # str or str list : handler name is
    # one string of handler name
    # or list of handler name
    handler = han.ReportsHandler(handler=user_params["handler"])
    data = handler.handle(data_in, params)
    filters = user_params["filters"]

    return {"data": data, "filters": filters}
