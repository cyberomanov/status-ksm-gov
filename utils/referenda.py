import json

import cloudscraper

from datatypes.response import *


def get_referenda_index(referenda: list[ReferendaItem]) -> list[int]:
    indexes = []
    for item in referenda:
        indexes.append(item.referendum_index)
    return indexes


def get_active_proposal() -> list[ReferendaItem]:
    url = "https://kusama.webapi.subscan.io/api/scan/referenda/referendums"
    referenda_pages = []
    page_index = 0
    while True:
        data = {
            "origin": "all",
            "page": page_index,
            "row": 100,
            "status": "active"
        }
        response = cloudscraper.create_scraper().post(url=url, json=data)
        page_response = ReferendaResponse.parse_obj(json.loads(response.content))
        if not page_response.data.list:
            break
        else:
            page_index += 1
            referenda_pages.append(page_response)

    proposals = []
    for referenda_page in referenda_pages:
        proposals = proposals + referenda_page.data.list
    return proposals


def get_referenda_voters(index: int) -> list[ReferendaItem]:
    url = f"https://kusama.webapi.subscan.io/api/scan/referenda/votes"
    referenda_pages = []
    page_index = 0

    while True:
        data = {
            "row": 100,
            "page": page_index,
            "referendum_index": index
        }
        response = cloudscraper.create_scraper().post(url=url, json=data)
        page_response = ReferendaResponse.parse_obj(json.loads(response.content))
        if not page_response.data.list:
            break
        else:
            page_index += 1
            referenda_pages.append(page_response)

    voters = []
    for referenda_page in referenda_pages:
        voters = voters + referenda_page.data.list
    return voters


def get_unvoted_proposals(indexes: list[int], stash: list[str]) -> dict:
    stashes = stash
    unvoted = {}

    for index in indexes:
        voters = get_referenda_voters(index=index)
        for stash in stashes:
            voted = False
            for voter in voters:
                if voter.account.address == stash:
                    voted = True
                    break
            if not voted:
                if stash in unvoted:
                    unvoted[stash] = unvoted[stash] + [index]
                else:
                    unvoted[stash] = [index]
    return unvoted


def get_identity(address: str) -> str:
    url = "https://kusama.webapi.subscan.io/api/v2/scan/search"
    data = {
        "key": address,
        "page": 0,
        "row": 1
    }
    response = cloudscraper.create_scraper().post(url=url, json=data)
    return ReferendaResponse.parse_obj(json.loads(response.content)).data.account.display
