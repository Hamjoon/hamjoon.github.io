// English is the default. Only an explicit language choice is persisted.
(() => {
  "use strict";
  const messages = {
  "skip": {
    "en": "Skip to content",
    "ko": "본문으로 건너뛰기"
  },
  "studio": {
    "en": "Garibong Labs",
    "ko": "가리봉랩스"
  },
  "nav.ios": {
    "en": "iOS Apps",
    "ko": "iOS 앱"
  },
  "nav.toss": {
    "en": "Toss Mini Apps",
    "ko": "토스 미니앱"
  },
  "nav.journal": {
    "en": "Journal",
    "ko": "개발 기록"
  },
  "nav.about": {
    "en": "About",
    "ko": "소개"
  },
  "nav.explore": {
    "en": "Explore work",
    "ko": "앱 둘러보기"
  },
  "hero.eyebrow": {
    "en": "Independent software studio · Seoul",
    "ko": "서울의 독립 소프트웨어 스튜디오"
  },
  "hero.line1": {
    "en": "Small software.",
    "ko": "작은 소프트웨어,"
  },
  "hero.line2": {
    "en": "Built to matter.",
    "ko": "의미 있는 경험."
  },
  "hero.description": {
    "en": "We design focused apps and playful experiences that turn everyday moments into something useful, calm, and memorable.",
    "ko": "일상의 순간을 더 유용하고 편안하게, 오래 기억할 수 있게 만드는 앱과 즐거운 경험을 설계해요."
  },
  "hero.explore": {
    "en": "Explore our work",
    "ko": "우리가 만든 앱"
  },
  "hero.journal": {
    "en": "Read the journal",
    "ko": "개발 기록 읽기"
  },
  "ios.eyebrow": {
    "en": "01 · iOS Apps",
    "ko": "01 · iOS 앱"
  },
  "ios.title": {
    "en": "Made for the App Store.",
    "ko": "App Store에서 만나요."
  },
  "ios.description": {
    "en": "Thoughtful utilities and original games, designed and built independently from first sketch to release.",
    "ko": "실용적인 도구부터 개성 있는 게임까지. 첫 스케치부터 출시까지 직접 기획하고 만들어요."
  },
  "ios.featured": {
    "en": "Featured · Reading",
    "ko": "추천 · 독서"
  },
  "app.book": {
    "en": "Book Lawn",
    "ko": "독서 잔디"
  },
  "app.book.description": {
    "en": "A quiet reading tracker that turns every reading session into a lawn you can grow over time.",
    "ko": "책을 읽는 시간이 차곡차곡 쌓여 나만의 잔디밭이 되는 독서 기록 앱이에요."
  },
  "ios.store.featured": {
    "en": "View on the App Store",
    "ko": "App Store에서 보기"
  },
  "category.sports": {
    "en": "Sports",
    "ko": "스포츠"
  },
  "app.asian": {
    "en": "2026 Asian Games",
    "ko": "2026 아시안게임"
  },
  "app.asian.description": {
    "en": "Team Korea schedules, medal events, and calendar reminders without the noise.",
    "ko": "대한민국 경기 일정과 메달 종목, 캘린더 알림을 한곳에서 확인해요."
  },
  "ios.store": {
    "en": "App Store",
    "ko": "App Store"
  },
  "category.music": {
    "en": "Music",
    "ko": "음악"
  },
  "app.radio": {
    "en": "Garibong Radio",
    "ko": "가리봉 라디오"
  },
  "app.radio.description": {
    "en": "Set a 24-hour radio schedule for focus, rest, jazz, classics, and sleep.",
    "ko": "집중과 휴식, 재즈와 클래식, 수면까지. 하루 24시간의 라디오 편성표를 만들어요."
  },
  "category.racing": {
    "en": "Game · Racing",
    "ko": "게임 · 레이싱"
  },
  "app.bloom": {
    "en": "Bloom Velocity",
    "ko": "블룸 벨로시티"
  },
  "app.bloom.description": {
    "en": "Fast anti-gravity combat racing above the bioluminescent oceans of an alien world.",
    "ko": "빛나는 외계 바다 위를 질주하는 반중력 컴뱃 레이싱 게임이에요."
  },
  "category.sportsgame": {
    "en": "Game · Sports",
    "ko": "게임 · 스포츠"
  },
  "app.tennis": {
    "en": "Lunch Table Tennis King",
    "ko": "점심 탁구왕"
  },
  "app.tennis.description": {
    "en": "One-handed 3D table tennis in an office lunch league. Beat four coworkers and become the lunch-break champion.",
    "ko": "한 손으로 즐기는 사내 점심 리그 3D 탁구. 동료 네 명을 이기고 점심시간의 챔피언이 되어 보세요."
  },
  "category.puzzle": {
    "en": "Game · Puzzle",
    "ko": "게임 · 퍼즐"
  },
  "app.tile": {
    "en": "Tile Trio",
    "ko": "타일 트리오"
  },
  "app.tile.description": {
    "en": "A relaxing triple-match puzzle across tropical islands. Play 60 levels and a daily challenge in English or Korean.",
    "ko": "열대 섬에서 느긋하게 즐기는 3매치 퍼즐. 60개 레벨과 매일 새로운 도전을 영어와 한국어로 즐겨요."
  },
  "toss.eyebrow": {
    "en": "02 · Toss Mini Apps",
    "ko": "02 · 토스 미니앱"
  },
  "toss.title": {
    "en": "Instant ideas, ready to play.",
    "ko": "토스에서 바로 만나는 즐거움."
  },
  "toss.description": {
    "en": "Explore thirteen mini apps made for everyday curiosity, quick decisions, and a little fun. View details on desktop or open directly in Toss on mobile.",
    "ko": "일상의 호기심과 작은 결정, 가벼운 재미를 위한 미니앱 13개를 만나보세요. PC에서는 상세 정보를, 모바일에서는 토스 앱을 바로 열 수 있어요."
  },
  "toss.tennis.description": {
    "en": "Play a quick office table tennis match.",
    "ko": "점심시간 사무실에서 탁구 한 판."
  },
  "toss.open": {
    "en": "Open in Toss",
    "ko": "토스에서 열기"
  },
  "toss.details": {
    "en": "View details",
    "ko": "상세보기"
  },
  "toss.reading": {
    "en": "Reading Lawn",
    "ko": "독서 잔디밭"
  },
  "toss.reading.description": {
    "en": "Grow a lawn through reading.",
    "ko": "책을 읽으며 나만의 잔디밭을 가꿔요."
  },
  "toss.movie": {
    "en": "Movie of the Week",
    "ko": "이번주 개봉영화"
  },
  "toss.movie.description": {
    "en": "See what is new in theaters.",
    "ko": "이번 주 극장에 새로 걸리는 영화들."
  },
  "toss.offday": {
    "en": "Next Day Off",
    "ko": "다음 쉬는날"
  },
  "toss.offday.description": {
    "en": "Count down to the next break.",
    "ko": "다음 휴일까지 며칠 남았는지 한눈에."
  },
  "toss.vacation": {
    "en": "Vacation Safety",
    "ko": "휴가길 조심지도"
  },
  "toss.vacation.description": {
    "en": "Spot accident-prone roads.",
    "ko": "사고가 잦은 구간을 미리 확인해요."
  },
  "toss.bloom.description": {
    "en": "Race above an alien ocean.",
    "ko": "외계 바다 위를 시원하게 질주해요."
  },
  "toss.ghost": {
    "en": "Scary Ghost Leg",
    "ko": "공포의 사다리"
  },
  "toss.ghost.description": {
    "en": "Pick a winner in 3D.",
    "ko": "3D 사다리로 짜릿하게 당첨자를 정해요."
  },
  "toss.roulette": {
    "en": "Roulette Wheel",
    "ko": "룰렛 돌리기"
  },
  "toss.roulette.description": {
    "en": "Let the wheel make the call.",
    "ko": "고민되는 선택은 룰렛에 맡겨요."
  },
  "toss.seoul": {
    "en": "Seoul Time Travel",
    "ko": "서울 시간여행"
  },
  "toss.seoul.description": {
    "en": "Watch Gwanghwamun change.",
    "ko": "시간에 따라 달라지는 광화문을 만나요."
  },
  "toss.hangang": {
    "en": "Hangang Stroll",
    "ko": "한강변 여름 산책"
  },
  "toss.hangang.description": {
    "en": "Take a playful 3D walk.",
    "ko": "가볍게 떠나는 즐거운 3D 산책."
  },
  "toss.hope": {
    "en": "Hope Poll",
    "ko": "Hope 해석 투표"
  },
  "toss.hope.description": {
    "en": "Vote on the film's meaning.",
    "ko": "영화의 해석에 나의 한 표를 더해요."
  },
  "toss.noodles": {
    "en": "Noodles Gauge",
    "ko": "평냉 배터리"
  },
  "toss.noodles.description": {
    "en": "Charge up with cold noodles.",
    "ko": "시원한 평양냉면으로 에너지를 채워요."
  },
  "toss.korea": {
    "en": "Team Korea 2026",
    "ko": "아시안게임 일정"
  },
  "toss.korea.description": {
    "en": "Follow every Korean match.",
    "ko": "대한민국의 모든 경기를 함께해요."
  },
  "journal.eyebrow": {
    "en": "03 · Journal",
    "ko": "03 · 개발 기록"
  },
  "journal.title": {
    "en": "Notes from the build.",
    "ko": "만들며 남긴 기록."
  },
  "journal.description": {
    "en": "Architecture, experiments, and practical lessons from making independent software.",
    "ko": "독립 소프트웨어를 만들며 쌓은 설계와 실험, 실전에서 배운 것들을 기록해요."
  },
  "journal.featured": {
    "en": "Featured article · Architecture",
    "ko": "추천 글 · 아키텍처"
  },
  "journal.article": {
    "en": "Calling My AI Agent: Building a Voice Bridge with OpenClaw and Agora",
    "ko": "나의 AI 에이전트에게 전화하기: OpenClaw와 Agora로 음성 연결 만들기"
  },
  "journal.summary": {
    "en": "A field note on the architecture and decisions behind connecting an AI agent to a real-time voice experience.",
    "ko": "AI 에이전트를 실시간 음성 경험에 연결하면서 고민한 구조와 설계 결정을 정리했어요."
  },
  "journal.read": {
    "en": "Read the article",
    "ko": "글 읽기"
  },
  "about.eyebrow": {
    "en": "04 · About",
    "ko": "04 · 소개"
  },
  "about.title": {
    "en": "Independent by design.",
    "ko": "독립적으로, 우리답게."
  },
  "about.description": {
    "en": "Garibong Labs is a Seoul-based independent software studio. We make small, focused products with equal care for usefulness, character, and long-term quality.",
    "ko": "가리봉랩스는 서울에 기반을 둔 독립 소프트웨어 스튜디오예요. 유용함과 개성, 오래가는 품질을 소중히 여기며 작고 명확한 제품을 만들어요."
  },
  "about.contact": {
    "en": "Contact us",
    "ko": "문의하기"
  },
  "about.github": {
    "en": "GitHub",
    "ko": "GitHub"
  },
  "footer.location": {
    "en": "Independent software studio · Seoul, Korea",
    "ko": "대한민국 서울 · 독립 소프트웨어 스튜디오"
  },
  "footer.email": {
    "en": "contact@garibong.dev",
    "ko": "contact@garibong.dev"
  },
  "footer.privacy": {
    "en": "Privacy Policy",
    "ko": "개인정보 처리방침"
  },
  "footer.business": {
    "en": "Business Registration Number: 604-05-36402",
    "ko": "사업자등록번호: 604-05-36402"
  },
  "footer.copyright": {
    "en": "© 2026 Garibong Labs. All rights reserved.",
    "ko": "© 2026 가리봉랩스. 모든 권리 보유."
  },
  "a11y.0": {
    "en": "Garibong Labs, home",
    "ko": "가리봉랩스 홈"
  },
  "a11y.1": {
    "en": "Primary navigation",
    "ko": "주요 메뉴"
  },
  "a11y.2": {
    "en": "Book Lawn and Bloom Velocity app previews",
    "ko": "독서 잔디와 블룸 벨로시티 앱 미리보기"
  },
  "a11y.3": {
    "en": "Book Lawn reading tracker screen",
    "ko": "독서 잔디 독서 기록 화면"
  },
  "a11y.4": {
    "en": "Bloom Velocity anti-gravity racing game screen",
    "ko": "블룸 벨로시티 반중력 레이싱 게임 화면"
  },
  "a11y.5": {
    "en": "View on the App Store — Book Lawn",
    "ko": "App Store에서 독서 잔디 보기"
  },
  "a11y.6": {
    "en": "View 2026 Asian Games on the App Store",
    "ko": "App Store에서 2026 아시안게임 보기"
  },
  "a11y.7": {
    "en": "View Garibong Radio on the App Store",
    "ko": "App Store에서 가리봉 라디오 보기"
  },
  "a11y.8": {
    "en": "View Bloom Velocity on the App Store",
    "ko": "App Store에서 블룸 벨로시티 보기"
  },
  "a11y.9": {
    "en": "View Lunch Table Tennis King on the App Store",
    "ko": "App Store에서 점심 탁구왕 보기"
  },
  "a11y.10": {
    "en": "View Tile Trio on the App Store",
    "ko": "App Store에서 타일 트리오 보기"
  },
  "a11y.11": {
    "en": "Live Toss mini apps",
    "ko": "서비스 중인 토스 미니앱"
  },
  "a11y.12": {
    "en": "Open in Toss — Lunch Table Tennis King",
    "ko": "토스에서 점심 탁구왕 열기"
  },
  "a11y.13": {
    "en": "View details — Lunch Table Tennis King (opens in a new tab)",
    "ko": "점심 탁구왕 상세보기 (새 탭에서 열림)"
  },
  "a11y.14": {
    "en": "Open in Toss — Reading Lawn",
    "ko": "토스에서 독서 잔디밭 열기"
  },
  "a11y.15": {
    "en": "View details — Reading Lawn (opens in a new tab)",
    "ko": "독서 잔디밭 상세보기 (새 탭에서 열림)"
  },
  "a11y.16": {
    "en": "Open in Toss — Movie of the Week",
    "ko": "토스에서 이번주 개봉영화 열기"
  },
  "a11y.17": {
    "en": "View details — Movie of the Week (opens in a new tab)",
    "ko": "이번주 개봉영화 상세보기 (새 탭에서 열림)"
  },
  "a11y.18": {
    "en": "Open in Toss — Next Day Off",
    "ko": "토스에서 다음 쉬는날 열기"
  },
  "a11y.19": {
    "en": "View details — Next Day Off (opens in a new tab)",
    "ko": "다음 쉬는날 상세보기 (새 탭에서 열림)"
  },
  "a11y.20": {
    "en": "Open in Toss — Vacation Safety",
    "ko": "토스에서 휴가길 조심지도 열기"
  },
  "a11y.21": {
    "en": "View details — Vacation Safety (opens in a new tab)",
    "ko": "휴가길 조심지도 상세보기 (새 탭에서 열림)"
  },
  "a11y.22": {
    "en": "Open in Toss — Bloom Velocity",
    "ko": "토스에서 블룸 벨로시티 열기"
  },
  "a11y.23": {
    "en": "View details — Bloom Velocity (opens in a new tab)",
    "ko": "블룸 벨로시티 상세보기 (새 탭에서 열림)"
  },
  "a11y.24": {
    "en": "Open in Toss — Scary Ghost Leg",
    "ko": "토스에서 공포의 사다리 열기"
  },
  "a11y.25": {
    "en": "View details — Scary Ghost Leg (opens in a new tab)",
    "ko": "공포의 사다리 상세보기 (새 탭에서 열림)"
  },
  "a11y.26": {
    "en": "Open in Toss — Roulette Wheel",
    "ko": "토스에서 룰렛 돌리기 열기"
  },
  "a11y.27": {
    "en": "View details — Roulette Wheel (opens in a new tab)",
    "ko": "룰렛 돌리기 상세보기 (새 탭에서 열림)"
  },
  "a11y.28": {
    "en": "Open in Toss — Seoul Time Travel",
    "ko": "토스에서 서울 시간여행 열기"
  },
  "a11y.29": {
    "en": "View details — Seoul Time Travel (opens in a new tab)",
    "ko": "서울 시간여행 상세보기 (새 탭에서 열림)"
  },
  "a11y.30": {
    "en": "Open in Toss — Hangang Stroll",
    "ko": "토스에서 한강변 여름 산책 열기"
  },
  "a11y.31": {
    "en": "View details — Hangang Stroll (opens in a new tab)",
    "ko": "한강변 여름 산책 상세보기 (새 탭에서 열림)"
  },
  "a11y.32": {
    "en": "Open in Toss — Hope Poll",
    "ko": "토스에서 Hope 해석 투표 열기"
  },
  "a11y.33": {
    "en": "View details — Hope Poll (opens in a new tab)",
    "ko": "Hope 해석 투표 상세보기 (새 탭에서 열림)"
  },
  "a11y.34": {
    "en": "Open in Toss — Noodles Gauge",
    "ko": "토스에서 평냉 배터리 열기"
  },
  "a11y.35": {
    "en": "View details — Noodles Gauge (opens in a new tab)",
    "ko": "평냉 배터리 상세보기 (새 탭에서 열림)"
  },
  "a11y.36": {
    "en": "Open in Toss — Team Korea 2026",
    "ko": "토스에서 아시안게임 일정 열기"
  },
  "a11y.37": {
    "en": "View details — Team Korea 2026 (opens in a new tab)",
    "ko": "아시안게임 일정 상세보기 (새 탭에서 열림)"
  },
  "page.title": {
    "en": "Garibong Labs · Independent Software Studio",
    "ko": "가리봉랩스 · 독립 소프트웨어 스튜디오"
  },
  "page.description": {
    "en": "Garibong Labs is an independent software studio in Seoul, building thoughtful iOS apps, playful games, and Toss mini apps.",
    "ko": "서울의 독립 소프트웨어 스튜디오 가리봉랩스. 실용적인 iOS 앱, 즐거운 게임, 토스 미니앱을 만들어요."
  },
  "page.ogTitle": {
    "en": "Garibong Labs · Small software. Built to matter.",
    "ko": "가리봉랩스 · 작은 소프트웨어, 의미 있는 경험."
  },
  "page.ogDescription": {
    "en": "Thoughtful iOS apps, playful games, and Toss mini apps from an independent studio in Seoul.",
    "ko": "서울의 독립 스튜디오가 만드는 유용한 iOS 앱과 즐거운 게임, 토스 미니앱."
  }
};
  const storageKey = "garibong.language";
  const controls = document.querySelector(".language-switch");
  const translate = (key, language) => messages[key]?.[language] ?? messages[key]?.en;
  function setLanguage(language) {
    if (language !== "ko") language = "en";
    document.documentElement.lang = language;
    document.querySelectorAll("[data-i18n]").forEach((element) => {
      const value = translate(element.dataset.i18n, language);
      if (value !== undefined) element.textContent = value;
    });
    for (const attribute of ["aria-label", "alt"]) {
      document.querySelectorAll(`[data-i18n-${attribute}]`).forEach((element) => {
        const value = translate(element.getAttribute(`data-i18n-${attribute}`), language);
        if (value !== undefined) element.setAttribute(attribute, value);
      });
    }
    document.title = translate("page.title", language);
    for (const [selector, key] of [
      ['meta[name="description"]', "page.description"],
      ['meta[property="og:title"]', "page.ogTitle"],
      ['meta[property="og:description"]', "page.ogDescription"]
    ]) document.querySelector(selector)?.setAttribute("content", translate(key, language));
    controls.setAttribute("aria-label", language === "ko" ? "언어" : "Language");
    controls.querySelectorAll("button").forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.language === language));
    });
  }
  let savedLanguage;
  try { savedLanguage = localStorage.getItem(storageKey); } catch { /* Storage may be unavailable. */ }
  setLanguage(savedLanguage === "ko" ? "ko" : "en");
  controls.hidden = false;
  controls.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-language]");
    if (!button || !controls.contains(button)) return;
    const language = button.dataset.language;
    setLanguage(language);
    try { localStorage.setItem(storageKey, language); } catch { /* Switching works without persistence. */ }
  });
})();
