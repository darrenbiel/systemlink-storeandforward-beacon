from datetime import datetime
import dateutil.parser
import glob
import json
import os


def calculate_pending_requests(storeDirectory: str) -> int:
    """
    Calculate the pending requests to be forwarded in the store and forward directory.

    :param storeDirectory: The data directory store and forward requests are stored in.
    :return: The quantity of requests pending to be forwarded.
    """
    if not os.path.isdir(storeDirectory):
        return 0

    cacheFilePath = os.path.join(storeDirectory, "__CACHE__")
    if not os.path.isfile(cacheFilePath):
        return 0

    lastProcessedTimestamp = _read_last_processed_timestamp(cacheFilePath)
    pending = 0
    transactionBufferPaths = glob.glob(os.path.join(storeDirectory, "*.jsonl"))
    for transactionBufferPath in transactionBufferPaths:
        pending += _count_transactions_after(transactionBufferPath, lastProcessedTimestamp)

    return pending


def calculate_quaratine_requests(storeDirectory: str) -> int:
    return 0


def _read_last_processed_timestamp(cacheFilePath: str) -> datetime:
    with open(cacheFilePath, "r", encoding="ansi") as cacheFile:
        cacheFileJson = json.load(cacheFile)
        return dateutil.parser.isoparse(cacheFileJson["timestamp"])


def _count_transactions_after(transactionBufferPath: str, lastProcessedTimestamp: datetime):
    lines = []
    with open(transactionBufferPath, "r", encoding="ansi") as transactionBuffer:
        lines = transactionBuffer.readlines()

    transactions = map(lambda line: json.loads(line), lines)
    newTransactions = filter(
        lambda t: lastProcessedTimestamp <= dateutil.parser.isoparse(t["timestamp"]), transactions
    )
    return len(list(newTransactions))