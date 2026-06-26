import streamlit as st
import requests
import xml.etree.ElementTree as ET # API가 XML 형식일 경우
import google.generativeai as genai
import xml.etree.ElementTree as ET



api_key_ai = st.secrets["API_KEY_AI"]


CONFIRM_KEY= st.secrets["API_KEY_DATA"]

st.markdown("""
    <style>

    /* 전체 배경 */
    .stApp{
        background: linear-gradient(
            135deg,
            #f7fff8,
            #eefcf2
        );
    }

    </style>

""", unsafe_allow_html=True)


# 2. 현재 페이지를 '숫자'로 기억하기 (처음엔 0번 페이지)
if "page" not in st.session_state:
    st.session_state.page = 0
if "search_results" not in st.session_state:
    st.session_state.search_results = None


# 3. 버튼을 누르면 페이지 번호를 바꿔주는 함수
def go_to_page(page_number):
    st.session_state.page = page_number


# =========================
# 코드표 변환
# =========================

drainage_map = {
    "01": "매우양호",
    "02": "양호",
    "03": "약간양호",
    "04": "약간불량",
    "05": "불량",
    "06": "매우불량"
}

depth_map = {
    "01": "0~25cm",
    "02": "25~50cm",
    "03": "50~100cm",
    "04": "100cm 이상"
}

texture_map = {
    "01": "양질조사토",
    "02": "양질세사토",
    "03": "양질사토",
    "04": "세사양토",
    "05": "사양토",
    "06": "양토",
    "07": "미사질양토",
    "08": "미사질식양토",
    "09": "식양토"
}

terrain_map = {
    "01": "산악지",
    "02": "구릉지",
    "03": "산록경사지",
    "04": "곡간지/선상지",
    "05": "해성평탄지",
    "06": "하성평탄지",
    "07": "고원지",
    "08": "홍적대지",
    "09": "용암류대지",
    "10": "용암류평탄"
}

landuse_map = {
    "01": "논",
    "02": "밭",
    "03": "과수/상전",
    "04": "간이초지",
    "05": "집약초지",
    "06": "임지"
}

grade_map = {
    "01": "1급지",
    "02": "2급지",
    "03": "3급지",
    "04": "4급지",
    "05": "5급지"
}

factor_map = {
    "00": "제외",
    "01": "없음",
    "02": "경사",
    "03": "저습",
    "04": "사질",
    "05": "석력",
    "09": "중점",
    "10": "경반",
    "11": "암반",
    "13": "화산회",
    "14": "배수불량"
}


# 1. 페이지 번호와 화면에 보여줄 이름을 연결하는 딕셔너리 (사전) 만들기
page_names = {
    0: "🏠 홈 (서비스 소개)",
    1: "1. 재배 환경 입력",
    2: "2. 농부 성향 입력",
    3: "3. 맞춤 작물 추천",
    4: "4. AI 농사 상담소"
}






# ==========================================
# 0. 홈 화면
# ==========================================
if st.session_state.page == 0:
        
    st.markdown("""
    <style>


    /* 전체 배경 */
    .stApp{
        background: linear-gradient(
            135deg,
            #f7fff8,
            #eefcf2
        );
    }

    /* Hero 카드 */
    .hero-card{
        background:white;
        padding:60px;
        border-radius:30px;
        box-shadow:0 10px 30px rgba(0,0,0,0.08);
        margin-bottom:30px;
    }

    /* 배지 */
    .badge{
        display:inline-block;
        background:#e8f9ed;
        color:#22c55e;
        padding:10px 18px;
        border-radius:999px;
        font-weight:700;
        margin-bottom:20px;
    }

    /* 제목 */
    .hero-title{
        font-size:55px;
        font-weight:800;
        line-height:1.2;
    }

    .hero-green{
        color:#22c55e;
    }

    /* 설명 */
    .hero-desc{
        font-size:22px;
        color:#555;
        margin-top:15px;
    }

    /* 추천 카드 */
    .info-card{
        background:white;
        padding:25px;
        border-radius:20px;
        text-align:center;
        border:1px solid #e8e8e8;
        box-shadow:0 5px 15px rgba(0,0,0,0.05);
    }

    /* 통계 카드 */
    .stat-card{
        background:white;
        padding:25px;
        border-radius:20px;
        text-align:center;
        box-shadow:0 5px 15px rgba(0,0,0,0.05);
    }

    .stat-number{
        font-size:40px;
        font-weight:800;
        color:#22c55e;
    }

    .stat-text{
        color:#666;
    }
    div.stButton > button {
    background-color: #22c55e;
    color: white;
    height: 80px;
    border-radius: 16px;
    border: none;
    }

    div.stButton > button p {
        font-size: 30px !important;
        font-weight: 900 !important;
    }

    div.stButton > button:hover {
        background-color: #16a34a;
        transform: translateY(-2px);
    }
    </style>

    """, unsafe_allow_html=True)

    # Hero 영역
    st.markdown("""
    
    <div class="hero-card">
        <div class="badge">
        🌱 AI 기반 스마트 농업
        </div>
        <div class="hero-title">
        당신에게 딱 맞는<br>
        <span class="hero-green">작물을 추천해드립니다</span>
        </div>
        <div class="hero-desc">
        토양 상태, 재배 환경, 농부 성향을 분석하여<br>
        AI가 가장 적합한 작물을 추천합니다.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(
        "작물 추천 시작하기",
        use_container_width=True
    ):
        go_to_page(1)


    st.write("")
    st.write("")

    # 추천 대상
    st.subheader("💡 이런 분들에게 추천해요!")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="info-card">
        <h1>🏡</h1>
        <h3>주말 농장</h3>
        <p>무엇을 심을지 고민될 때</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
        <h1>🪴</h1>
        <h3>내 집 마당</h3>
        <p>집 앞 마당에서도 가능</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="info-card">
        <h1>👨‍🌾</h1>
        <h3>초보 농부</h3>
        <p>AI가 쉽게 안내해드려요</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")




# ==========================================
# 1페이지
# ==========================================
elif st.session_state.page == 1:
    


    st.title("어디서 키우실 건가요? 🏡")
    addrees = st.text_input("동/읍/면/리 를 입력해주세요")
    adm_cd=''
    if st.button("주소검색"):
        url = "https://apis.data.go.kr/1741000/StanReginCd/getStanReginCdList"
        params = {"ServiceKey": CONFIRM_KEY, "pageNo": 1, "numOfRows": 10, "type": "json", "locatadd_nm": addrees}

        response = requests.get(url, params=params).json()
        # st.write(response.text)
        st.session_state.search_results = response["StanReginCd"][1]['row']

    if st.session_state.get("search_results"):
        # API 응답 필드명에 맞춰 키값 수정 (locatadd_nm 사용)
        # options {= {f"{item['locatadd_nm']}": item for item in st.session_state.search_results}}
        options={}
        for item in st.session_state.search_results:
            options[item['locatadd_nm']]=item['region_cd']


        if options !="":
            selected = st.selectbox("정확한 주소를 선택하세요", list(options.keys()))
            adm_cd = options[selected]
            # adm_cd = selected_addr.get("region_cd"
        
    mount = st.radio("산인지 토지인지 선택하세요",['일반','산'])
    if mount == '일반':
        mountcode = 1
    else:
        mountcode = 2
        
    jibun = st.text_input('지번을 입력하세요')
    boobun = st.text_input('부번을 입력하세요')

    st.session_state.pnu = ( adm_cd + str(mountcode) + jibun.zfill(4) + boobun.zfill(4) )

    if st.button('다음'):
        go_to_page(2)
        




#============================================
# 수정 전 코드
#============================================    
#     st.title("어디서 키우실 건가요? 🏡")
#     st.write("📍카카오/행안부 주소 검색 API 연동")   
#     st.write("정확한 토양 분석을 위해 텃밭의 도로명이나 동 이름을 검색해주세요. (예: 둔산동, 판교역로)")
#    # 발급받은 승인키 입력
#     CONFIRM_KEY = "devU01TX0FVVEgyMDI2MDUzMDExMTMyODExODk2MzU="

#     st.title("도로명 주소 검색")

#     keyword = st.text_input("주소 검색", placeholder="예: 판교역로 235")

#     def search_address(keyword):
#         url = "https://business.juso.go.kr/addrlink/addrLinkApi.do"

#         params = {
#             "confmKey": CONFIRM_KEY,
#             "currentPage": 1,
#             "countPerPage": 20,
#             "keyword": keyword,
#             "resultType": "json"
#         }

#         response = requests.get(url, params=params)
#         response.raise_for_status()

#         data = response.json()
#         return data

#     if st.button("주소검색"):

#         try:
#             result = search_address(keyword)

#             common = result["results"]["common"]

#             if common["errorCode"] != "0":
#                 st.error(common["errorMessage"])

#             else:
#                 addresses = result["results"]["juso"]

#                 if not addresses:
#                     st.warning("검색 결과가 없습니다.")

#                 else:
#                     options = {
#                         f"{item['roadAddr']} ({item['zipNo']})": item
#                         for item in addresses
#                     }

#                     selected = st.selectbox(
#                         "정확한 주소를 선택하세요",
#                         list(options.keys())
#                     )

#                     selected_addr = options[selected]

#                     st.success("선택 완료")
           

#                     st.write("### 주소 정보")
#                     st.write("도로명주소:", selected_addr["roadAddr"])
#                     st.write("지번주소:", selected_addr["jibunAddr"])
#                     st.write("우편번호:", selected_addr["zipNo"])
#                     st.write("시도:", selected_addr["siNm"])
#                     st.write("시군구:", selected_addr["sggNm"])
#                     st.write("읍면동:", selected_addr["emdNm"])

#                     st.json(selected_addr)

#                     pnu = (
#                         str(selected_addr["admCd"])
#                         + ("2" if selected_addr["mtYn"] == "1" else "2")
#                         + str(selected_addr["lnbrMnnm"]).zfill(4)
#                         + str(selected_addr["lnbrSlno"]).zfill(4)
#                     )
                    
#                     st.write(pnu)
#                     st.session_state["pnu"] = pnu
#                     print("여긴 되나?")

#         except Exception as e:
#             st.error(str(e))

#     if st.button("다음"):
#         print("왜 안넘어가지?")
#         go_to_page(2)
#         st.rerun()

# ==========================================
# 2페이지
# ==========================================
elif st.session_state.page == 2:

    st.markdown("""
    <style>

    .stButton > button {
        width:100%;
        height:250px;
        min-width: 250px;   /* 추가 */
        border-radius:30px;
        border:2px solid #dfe8df;

        background:white;

        font-size:28px;
        font-weight:700;

        box-shadow:0 8px 20px rgba(0,0,0,0.06);

        transition:0.3s;
    }

    .stButton > button:hover {
        border:3px solid #22c55e;
        transform:translateY(-5px);
        box-shadow:0 12px 30px rgba(34,197,94,0.2);
    }

    </style>
    """, unsafe_allow_html=True)
    st.progress(50)

    st.markdown("""
    <div style='text-align:center;padding:20px'>
        <h1>🌱 얼마나 자주 가실 수 있나요?</h1>
        <p style='font-size:20px;color:gray'>
            방문 가능 횟수에 따라 추천 작물이 달라집니다
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3,gap="large")

    with col1:
        if st.button("🌱\n\n주 1회 이상\n\n자주 방문 가능",use_container_width=True):
  
            st.session_state.often = "주 1회 이상"
            go_to_page(3)
            st.rerun()

    with col2:
        if st.button("🌾\n\n2주에 1회\n\n보통 수준",use_container_width=True):
            st.session_state.often = "2주에 1회"
            go_to_page(3)
            st.rerun()

    with col3:
        if st.button("🍅\n\n한 달에 1회\n\n가끔 방문 가능",use_container_width=True):
            st.session_state.often = "한 달에 1회"
            go_to_page(3)
            st.rerun()


# ===========================
# 3page 목적 선택 페이지
# ===========================
elif st.session_state.page == 3:
    
    st.markdown("""
    <style>

    .stButton > button {
        width:100%;
        height:250px;
        min-width: 150px;   /* 추가 */
        border-radius:30px;
        border:2px solid #dfe8df;

        background:white;

        font-size:28px;
        font-weight:700;

        box-shadow:0 8px 20px rgba(0,0,0,0.06);

        transition:0.3s;
    }

    .stButton > button:hover {
        border:3px solid #22c55e;
        transform:translateY(-5px);
        box-shadow:0 12px 30px rgba(34,197,94,0.2);
    }

    </style>
                
    """, unsafe_allow_html=True)


    st.progress(75)

    
    st.markdown("""
    <div style='text-align:center;padding:20px'>
        <h1>🌱 작물을 키우는 목적은 무엇인가요?</h1>
        <p style='font-size:20px;color:gray'>
        목적에 따라 추천 작물이 달라집니다
        </p>
    </div>
    """, unsafe_allow_html=True)

    
    col1, col2, col3, col4 = st.columns(4, gap="large")



    
    with col1:
        if st.button(  "🧅\n\n식비 절약",use_container_width=True):
            st.session_state.purpose = "식비 절약"
            go_to_page(4)
            st.rerun()

    with col2:
        if st.button(
            "😄\n\n관상용 및 힐링",
            use_container_width=True
        ):
            st.session_state.purpose = "관상용 및 힐링"
            go_to_page(4)
            st.rerun()

    with col3:
        if st.button(
            "🥩🥬\n\n삼겹살 파티용",
            use_container_width=True
        ):
            st.session_state.purpose = "삼겹살 파티용"
            go_to_page(4)
            st.rerun()

    with col4:
        if st.button(
            "👦\n\n아이들 교육용",
            use_container_width=True
        ):
            st.session_state.purpose = "아이들 교육용"
            go_to_page(4)
            st.rerun()



# ==========================================
# 4페이지
# ==========================================
elif st.session_state.page == 4:
    st.title("당신을 위한 맞춤 작물 🍅")

   

    def get_soil_data(pnu_code, service_key):
    # API 요청 URL (기술명세서에 있는 엔드포인트 주소)
       
        url = "http://apis.data.go.kr/1390802/SoilEnviron/SoilCharac/V3/getSoilCharacter"
   
    # 전달할 파라미터 (지번코드, 서비스키 등)
        params = {
            'serviceKey': service_key,
            'PNU_CD': pnu_code,
       
        }
       
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.text # 성공 시 데이터 반환
            else:
                return None
        except Exception as e:
            return str(e)
    



   
    
# =========================
# Gemini에 전달할 데이터
# =========================


    if st.button("나에게 맞는 작물 찾기"):
        with st.spinner("🌱 토양 정보를 분석하는 중입니다..."):
            result = get_soil_data(st.session_state["pnu"], CONFIRM_KEY)
        
        if result:
            root = ET.fromstring(result)
            item = root.find(".//item")
            soil_data = {
        "배수등급": drainage_map.get(
            item.findtext("Soildra_Cd"),
            "알수없음"
        ),

        "유효토심": depth_map.get(
            item.findtext("Vldsoildep_Cd"),
            "알수없음"
        ),

        "표토토성": texture_map.get(
            item.findtext("Surtture_Cd"),
            "알수없음"
        ),

        "분포지형": terrain_map.get(
            item.findtext("Soil_Type_Geo_Cd"),
            "알수없음"
        ),

        "토지이용추천": landuse_map.get(
            item.findtext("Soil_Use_Rec_Cd"),
            "알수없음"
        ),

        "밭적성등급": grade_map.get(
            item.findtext("Pfld_Grd_Cd"),
            "알수없음"
        ),

        "과수적성등급": grade_map.get(
            item.findtext("Fruit_Grd_Cd"),
            "알수없음"
        ),

        "밭저해요인": factor_map.get(
            item.findtext("Upland_Factor_Cd"),
            "알수없음"
        ),

        "과수저해요인": factor_map.get(
            item.findtext("Fruit_Factor_Cd"),
            "알수없음"
        )
    }
            print(soil_data)
            genai.configure(api_key=api_key_ai)
            model = genai.GenerativeModel('gemini-3.5-flash', request_options={"timeout": 120} )
            context = f"""
                너는 전문 농업 컨설턴트이다.

                사용자는 초보 농부이다.

                방문 가능 빈도:
                {st.session_state["often"]}

                재배 목적:
                {st.session_state["purpose"]}

                토양 정보:
                {soil_data}

                판단 기준:

                - 방문 가능 빈도가 낮으면 관리가 쉬운 작물을 우선 추천
                - 방문 가능 빈도가 높으면 관리가 필요한 작물도 추천 가능
                - 식비 절약이면 수확량이 많고 활용도가 높은 작물 우선
                - 관상용 및 힐링이면 보기 좋고 키우기 쉬운 작물 우선
                - 삼겹살 파티용이면 상추, 깻잎 등 쌈채소 계열 우선
                - 아이들 교육용이면 성장 과정이 잘 보이는 작물 우선
                - 더 간결하게 한 작물당 3줄 정도로 보기 쉽게

                위 조건과 토양 정보를 함께 고려하여
                작물 TOP3를 추천하시오.
                """
            with st.spinner("🤖 AI가 작물을 추천하는 중입니다..."):
                response=model.generate_content(context)
            st.write(response.text)

        else:
            st.error("데이터 불러오기 실패")
            


























