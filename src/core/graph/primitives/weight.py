from typing import Protocol, Self, runtime_checkable


@runtime_checkable
class Weight(Protocol):
    """가중치로 사용할 수 있는 타입의 프로토콜.

    ``int``, ``float`` 등 덧셈과 대소 비교가 가능한 타입이면 모두 가중치로 쓸 수 있다.
    ``@runtime_checkable`` 이므로 ``isinstance`` 및 ``match/case`` 패턴 매칭에서
    구조적 서브타이핑 검사가 런타임에도 동작한다.
    """

    def __add__(self, other: Self, /) -> Self: ...
    def __lt__(self, other: Self, /) -> bool: ...
    def __le__(self, other: Self, /) -> bool: ...
