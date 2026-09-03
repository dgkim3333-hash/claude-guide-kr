"""
apis 패키지 초기화.

여기서 import하면 각 파일의 register(...) 호출이 실행되어
core.registry의 전역 레지스트리에 ApiSpec이 추가됨.

새 API 파일 추가 시:
  1. apis/xxx.py 생성
  2. 이 파일에 `from . import xxx` 한 줄 추가
"""
from . import epost_address      # 우편사업본부 도로명주소
from . import legal_dong         # 행안부 법정동코드
from . import building           # 건축HUB 건축물대장 (9 endpoints)
from . import molit_realprice    # 국토부 실거래가 (12 endpoints)
from . import onbid              # 캠코 온비드 (19 endpoints)
from . import sbiz_commercial    # 소상공인 상가정보
from . import housing_transport  # 공동주택 단지 + 도시철도

__all__: list = []
