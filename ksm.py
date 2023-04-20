from loguru import logger

from sdk.telegram import Telegram
from utils.add_logger import add_logger
from utils.get_config import *
from utils.referenda import *

if __name__ == '__main__':
    add_logger()
    try:
        config = get_config()
        settings, stash = config.settings, config.stash
        telegram = Telegram(bot_api_token=settings.bot_api_key, log_chat_id=settings.log_chat_id)

        referenda_v1 = get_active_v1_proposal()
        referenda_v2 = get_active_v2_proposal()

        if len(referenda_v1 + referenda_v2) > 0 and len(stash) > 0:
            unvoted_proposals_v1 = get_unvoted_proposals(indexes=get_referenda_index(referenda=referenda_v1),
                                                         stash=stash,
                                                         version=1)
            unvoted_proposals_v2 = get_unvoted_proposals(indexes=get_referenda_index(referenda=referenda_v2),
                                                         stash=stash,
                                                         version=2)
            
            unvoted_proposals = unvoted_proposals_v1.copy()
            for key, value in unvoted_proposals_v2.items():
                if key in unvoted_proposals:
                    unvoted_proposals[key].extend(value)
                else:
                    unvoted_proposals[key] = value

            if unvoted_proposals != {}:
                telegram_message = ''

                for unvoted in unvoted_proposals:
                    try:
                        identity = get_identity(address=unvoted)
                    except Exception as e:
                        identity = unvoted[:3] + '...' + unvoted[-3:]

                    message = f"{identity}: {', '.join(str(i) for i in unvoted_proposals[unvoted])}."
                    logger.info(message)
                    telegram_message += message + '\n'

                telegram_response = telegram.send_log(head='', body=telegram_message)
                if not telegram_response.ok:
                    logger.error(
                        f"telegram response is not ok. "
                        f"code: {telegram_response.error_code}, "
                        f"description: {telegram_response.description}."
                    )
                else:
                    logger.warning(f"telegram message successfully sent.")
            else:
                logger.info(f"there's no unvoted proposals.")
        else:
            logger.warning(f"there's no active proposals.")
    except Exception as e:
        logger.exception(e)
