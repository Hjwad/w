from functools import wraps
from threading import RLock
from time import perf_counter

from cachetools import TTLCache
from telegram import Chat, ChatMember, ChatMemberAdministrator, ChatMemberOwner, Update
from telegram.constants import ChatMemberStatus, ChatType
from telegram.error import Forbidden
from telegram.ext import CallbackContext

from Wolf import ASCETIC, SUPPORT_CHAT, dispatcher

# stores admemes in memory for 10 min.
ADMIN_CACHE = TTLCache(maxsize=512, ttl=60 * 10, timer=perf_counter)
THREAD_LOCK = RLock()


def admin_only(
    permission: str = None,
    is_bot: bool = False,
    is_user: bool = False,
    is_both: bool = False,
    only_owner: bool = False,
    only_sudo: bool = False,
    only_dev: bool = False,
    no_reply: object = False,
) -> object:
    """Check for permission level to perform some operations

    Args:
        permission (str, optional): permission type to check. Defaults to None.
        is_bot (bool, optional): if bot can perform the action. Defaults to False.
        is_user (bool, optional): if user can perform the action. Defaults to False.
        is_both (bool, optional): if both user and bot can perform the action. Defaults to False.
        only_owner (bool, optional): if only owner can perform the action. Defaults to False.
        only_sudo (bool, optional): if only sudo users can perform the operation. Defaults to False.
        only_dev (bool, optional): if only dev users can perform the operation. Defaults to False.
        no_reply (boot, optional): if should not reply. Defaults to False.
    """

    def wrapper(func):
        @wraps(func)
        async def wrapped(
            update: Update, context: CallbackContext, *args, **kwargs
        ):
            nonlocal permission
            chat = update.effective_chat
            user = update.effective_user
            message = update.effective_message

            if chat.type == ChatType.PRIVATE and not (
                only_dev or only_sudo or only_owner
            ):
                return await func(update, context, *args, **kwargs)

            bot_member = (
                await chat.get_member(context.bot.id) if is_bot or is_both else None
            )
            user_member = await chat.get_member(user.id) if is_user or is_both else None

            if only_owner:
                if isinstance(user_member, ChatMemberOwner) or user.id in ASCETIC:
                    return await func(update, context, *args, **kwargs)
                else:
                    return await message.reply_text(
                        "Only chat owner can perform this action."
                    )
            if only_sudo:
                if user.id in ASCETIC:
                    return await func(update, context, *args, **kwargs)
                else:
                    return await update.effective_message.reply_text(
                        "Who the hell are you to say me what to do?",
                    )
                
            if permission:
                no_permission = permission.replace("_", " ").replace("can", "")
                if is_bot:
                    if (
                        getattr(bot_member, permission)
                        if isinstance(bot_member, ChatMemberAdministrator)
                        else False
                    ):
                        return await func(update, context, *args, **kwargs)
                    elif no_reply:
                        return
                    else:
                        return await message.reply_text(
                            f"I don't have permission to {no_permission}."
                        )
                if is_user:
                    if isinstance(user_member, ChatMemberOwner):
                        return await func(update, context, *args, **kwargs)
                    elif (
                        getattr(user_member, permission)
                        if isinstance(user_member, ChatMemberAdministrator)
                        else False or user.id in ASCETIC
                    ):
                        return await func(update, context, *args, **kwargs)
                    elif no_reply:
                        return
                    else:
                        return await message.reply_text(
                            f"You don't have permission to {no_permission}."
                        )
                if is_both:
                    if (
                        getattr(bot_member, permission)
                        if isinstance(bot_member, ChatMemberAdministrator)
                        else False
                    ):
                        pass
                    elif no_reply:
                        return
                    else:
                        return await message.reply_text(
                            f"I don't have permission to {no_permission}."
                        )

                    if isinstance(user_member, ChatMemberOwner) or user.id in ASCETIC:
                        pass
                    elif (
                        getattr(user_member, permission)
                        if isinstance(user_member, ChatMemberAdministrator)
                        else False or user.id in ASCETIC
                    ):
                        pass
                    elif no_reply:
                        return
                    else:
                        return await message.reply_text(
                            f"You don't have permission to {no_permission}."
                        )
                    return await func(update, context, *args, **kwargs)
            else:
                if is_bot:
                    if bot_member.status == ChatMemberStatus.ADMINISTRATOR:
                        return await func(update, context, *args, **kwargs)
                    else:
                        return await message.reply_text("I'm not admin here.")
                elif is_user:
                    if user_member.status in [
                        ChatMemberStatus.ADMINISTRATOR,
                        ChatMemberStatus.OWNER,
                    ]:
                        return await func(update, context, *args, **kwargs)
                    elif user.id in ASCETIC:
                        return await func(update, context, *args, **kwargs)
                    else:
                        return await message.reply_text("You are not admin here.")
                elif is_both:
                    if bot_member.status == ChatMemberStatus.ADMINISTRATOR:
                        pass
                    else:
                        return await message.reply_text("I'm not admin here.")

                    if user_member.status in [
                        ChatMemberStatus.ADMINISTRATOR,
                        ChatMemberStatus.OWNER,
                    ]:
                        pass
                    elif user.id in ASCETIC:
                        pass
                    else:
                        return await message.reply_text("You are not admin here.")
                    return await func(update, context, *args, **kwargs)

        return wrapped

    return wrapper

def support_plus(chat: Chat, user_id: int, member: ChatMember = None) -> bool:
    return user_id in ASCETIC

async def is_user_admin(chat: Chat, user_id: int, member: ChatMember = None) -> bool:
    if (
        chat.type == "private"
        or user_id in ASCETIC
        or user_id in [777000, 1087968824]
    ):  # Count telegram and Group Anonymous as admin
        return True
    if not member:
        with THREAD_LOCK:
            # try to fetch from cache first.
            try:
                return user_id in ADMIN_CACHE[chat.id]
            except KeyError:
                # keyerror happend means cache is deleted,
                # so query bot api again and return user status
                # while saving it in cache for future usage...
                try:
                    chat_admins = await dispatcher.bot.getChatAdministrators(chat.id)
                except Forbidden:
                    return False
                admin_list = [x.user.id for x in chat_admins]
                ADMIN_CACHE[chat.id] = admin_list

                return user_id in admin_list
    else:
        return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)


async def is_bot_admin(chat: Chat, bot_id: int, bot_member: ChatMember = None) -> bool:
    if chat.type == "private":
        return True

    if not bot_member:
        bot_member = await chat.get_member(bot_id)

    return bot_member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)


def support(func):
    @wraps(func)
    async def support_func(
        update: Update, context: CallbackContext, *args, **kwargs
    ):
        user = update.effective_user
        chat = update.effective_chat

        if user and support_plus(chat, user.id):
            return await func(update, context, *args, **kwargs)
        else:
            update.effective_message.reply_text("You lack the authority to run this command.")

    return support_func