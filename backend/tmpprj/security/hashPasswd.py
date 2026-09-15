import hashlib

from tmpprj.config import settings


def hashPass(rowPasswd):
    rowPasswd += settings.passwd_salt
    hashPasswd = hashlib.sha1(rowPasswd.encode("utf-8")).hexdigest()
    return hashPasswd
