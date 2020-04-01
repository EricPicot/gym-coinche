class PlayException(Exception):
    pass


class MustPlayHigherAtout(PlayException):
    pass


class MustPlayCurrentSuit(PlayException):
    pass


class MustPlayAtout(PlayException):
    pass


class MustPlayACard(PlayException):
    pass


class MustPlayHisCards(PlayException):
    pass
