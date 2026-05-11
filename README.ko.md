# 사회학 연구 위키 (Sociology Research Wiki)

사회학자를 위한 LLM 보조 연구 위키 시스템입니다. **내용 정확성**을 *토큰 효율성이나 (AI 입장에서 판단하는) 문서 내 완결성*보다 우선하도록 설계되었습니다. 문헌 노트(literature notes), 연구자 본인의 아이디어 노트(atomic claims), 개념 페이지(concept pages), 프로젝트 허브를 누적하는 동시에, 환각(hallucination)으로 흘러가지 않도록 막아주는 규율을 함께 제공합니다.

이 템플릿이 정교하게 짜여졌지만, 개인의 위키 구축 과정에서 수많은 추가 설정과 점검이 필요합니다. 이걸 우회하는 어떤 제안도 사실이 아니라는 것을 기억하십시오.

[Karpathy의 LLM Wiki](https://gist.github.com/karpathy/1dd0294ef9567971c1e4348a90d69285)와 [joonan30의 adaptation](https://gist.github.com/joonan30/cbce305684d079dbe9a3fbaefe4e3959)에서 출발해 두 가지를 더했습니다.

1. **3계층 출처 검증 프로토콜 (Three-layer source verification)** — 위키의 모든 사실이 *로컬 원전 → 웹에서 다운로드한 원전 PDF → 빈칸*의 순서를 거칩니다. 2차 출처(리뷰 논문·교과서·초록·위키피디아·AI 요약)는 어느 단계에서도 사용할 수 없습니다.
2. **연구자 본인의 아이디어 노트 (Atomic claims layer)** — Ahrens가 말한 영구 노트(permanent note) 개념의 적용입니다. 원전 충실(source-faithful) 요약과 연구자 본인의 아이디어를 결합한 노트정리를 명시적으로 분리합니다.

본 시스템은 Claude Code 프로젝트로 동작합니다. 위키 자체는 plain markdown 형식이며 Obsidian과 호환됩니다. 스킬·메모리·스크립트가 함께 번들로 제공됩니다.

**언어**: 세 가지 구성을 지원합니다 — (A) 영어 전용(기본), (B) 단일 비영어 언어, (C) **본인 언어 + 영어 미러**(`---` 구분선으로 분리; 이중 언어 사용자와 영어권 공저자에게 유용). [`CLAUDE.md`](CLAUDE.md)의 Language Policy 섹션에서 선택합니다. 템플릿은 한국어를 적용 예시로 보여주며, 다른 언어로 자유롭게 치환할 수 있습니다. 참고문헌 요약은 언제나 원본 논문의 언어를 따릅니다.

영어 원본: [`README.md`](README.md)

---

## 왜 이 시스템이 필요한가

일반적인 문제는 LLM 보조 위키가 환각된 인용을 만들어낸다는 점입니다. *"Smith (2010)이 X를 보였다"*는데 그 논문이 존재하지 않거나, NLSY79와 NLSY97을 혼동하거나, 계수 `0.110`이 "약 50%"로 요약되는 패턴이 조용히 전파됩니다. 사회학에서 특히 위험한 이유는 다음과 같습니다.

- **오류가 누적됩니다.** 위키의 잘못된 설명이 문헌 검토(lit review)로 옮겨가고, 그것이 출간된 논문에 옮겨가며, 다시 다른 사람의 문헌 검토에 옮겨갑니다.
- **잘못된 문헌 검토가 반복됩니다.** 위키에 들어간 내용이 *수년간 본인 인용의 출처*가 됩니다.
- **잘못된 측정치를 알려주거나, 측정치의 정확한 의미가 사라집니다.** "효과 크기는 작았다"는 표현은 계수가 0.05인지 0.005인지 감춥니다.
- **이론의 특성을 잘못 기술합니다.** *"Hyper-selectivity는 문화 이론"*이라는 명제가 그럴듯하게 들리지만, Lee-Zhou는 명시적으로 문화적 frame을 반대합니다.

본 시스템은 이론 기반 정량 연구를 수행하는 사회학자를 위해 설계되었습니다. 사회학 메인 학술지에 투고하고, LLM의 도움이 필요할 만큼 많은 논문을 읽으며, 본인의 위키가 신뢰할 수 있는 인용 출처여야 하는 작업이 그 대상입니다.

검증 프로토콜과 binding rules는 다음과 같은 실패 모드에 대응합니다. 단 한 번의 인제스트 오류(예: 한 논문의 데이터 섹션을 그럴듯해 보이지만 조작된 내용으로 채우는 경우)가 여러 다운스트림 산출물로 연쇄적으로 퍼지고, 그것을 발견·수정하는 데 수개월이 걸리는 경우가 생깁니다. 본 시스템의 절차들은 그 연쇄를 위키 레이어에서 차단하는 것을 목적으로 합니다.

### 트레이드오프에 관하여

본 디자인은 **속도와 토큰 절약보다 내용 정확성을 우선합니다**. AI는 효율성을 추구하는 경향이 매우 강한데, 그럴듯해 보이는 어떤 효율성 추구도 — 정독 대신 훑어보기, 초록 기반 요약, 일괄 인제스트, "그럴듯해 보임"을 검증 없이 수용 — 모두 다운스트림에서 환각으로 이어집니다. 트레이드오프는 의도된 것입니다. 논문당 인제스트가 더 오래 걸리고 LLM 컨텍스트도 더 소비하지만, 위키에 들어가는 내용은 검증 가능한 상태가 됩니다. 검증 깊이를 희생하면서 시간을 절약하는 워크플로 변경을 하지 않는 것이 최선입니다.

---

## Repository 내용

| 폴더 | 목적 |
|------|------|
| [`CLAUDE.md`](CLAUDE.md) | Claude Code 메인 routing — 매 세션 Claude가 읽는 지침 |
| [`PHILOSOPHY.md`](PHILOSOPHY.md) / [`PHILOSOPHY.ko.md`](PHILOSOPHY.ko.md) | 설계 근거: 정확성 우선·5계층 노트·폴더 구조의 *왜* |
| [`QUICKSTART.md`](QUICKSTART.md) / [`QUICKSTART.ko.md`](QUICKSTART.ko.md) | 신규 연구자를 위한 10분 셋업 + 인제스트·린트 절차 |
| [`docs/`](docs/) | 핵심 문서 (노트 위계·검증 프로토콜·정확성 규칙·워크플로) |
| [`templates/`](templates/) | 모든 노트 유형의 마크다운 템플릿 (reference·concept·claim·project·category) |
| [`memory/`](memory/) | 영속 메모리 항목 — 피드백 규칙·참조·프로젝트 맥락 예시 포함 |
| [`indexes/`](indexes/) | Master 인덱스 파일 스켈레톤 (author index·concept index·master reference list·log) |
| [`scripts/`](scripts/) | 유지보수 스크립트: lint·prose→ref 자동 링크화·RAG 인덱서·link graph 진단 |

---

## 5계층 노트 위계

이 시스템의 핵심 설계 commitment입니다. 각 계층은 단일한 목소리(voice)를 가지며, 목소리가 섞이는 것이 단일 계층 위키에서 가장 흔히 나타나는 실패 모드입니다.

```
┌──────────────────────────────────────────────────────────────┐
│ Layer 5 — Index hubs (index.md, index_authors, index_detail)  │
│ Structure: navigation, dedup, status                          │
├──────────────────────────────────────────────────────────────┤
│ Layer 4 — Project hubs (projects/{year}/{name}/)              │
│ Voice: 본인, 프로젝트 한정                                       │
├──────────────────────────────────────────────────────────────┤
│ Layer 3 — Atomic claims (claims/)                             │
│ Voice: 본인, 합성된 — Ahrens permanent notes                    │
├──────────────────────────────────────────────────────────────┤
│ Layer 2 — Concept notes (general/{category}/)                 │
│ Voice: neutral, scholarly — 정의 + 실증 기록                    │
├──────────────────────────────────────────────────────────────┤
│ Layer 1 — Literature notes (references/)                      │
│ Voice: 저자의 — source-faithful, 본인 해석 금지                  │
├──────────────────────────────────────────────────────────────┤
│ Layer 0 — Raw sources (papers/papers_md/*.md from PDFs)                │
│ Read-only, never edit                                         │
└──────────────────────────────────────────────────────────────┘
```

핵심 아키텍처 규칙은 다음과 같습니다. claims(Layer 3)는 concepts(Layer 2) 위에 쌓이고, concepts는 references(Layer 1) 위에 쌓입니다. *역방향은 절대 금지*입니다. references 요약이 claim의 언어를 가져와서도 안 되고, claim이 references의 내용을 침묵 속에서 다시 써서도 안 됩니다.

5계층 구조의 근거: [`PHILOSOPHY.ko.md`](PHILOSOPHY.ko.md) → "왜 다섯 계층인가". 각 계층 템플릿: [`templates/`](templates/).

---

## 3계층 검증 프로토콜

위키에 들어가는 모든 사실(데이터셋 이름·표본 크기·회귀 계수·인용 계보·이론 귀속 등)은 *작성되기 전에* 이 프로토콜을 통과해야 합니다.

```
Layer 1 — 로컬 원전(PRIMARY SOURCE)
   논문 본문을 직접 읽음. papers/의 PDF와 papers/papers_md/{stem}.md (pymupdf4llm 변환본).
   ↓ 변환 깨짐 (스캔본·이미지 기반 PDF 등)
   OCR recovery: ocrmypdf 등으로 동일 PDF에서 텍스트 재추출 (Layer 1 안에서의 재시도)
   ↓ OCR도 실패하거나 PDF 자체가 없음
Layer 2 — 웹에서 다운로드한 원전
   웹에서 *논문의 PDF 자체*를 찾아 다운로드. papers_web/{stem}.pdf로 저장하고
   papers_web/papers_web_md/{stem}.md로 변환한 뒤 원전으로 취급함.
   웹은 **논문 자체의 PDF에 한해서만** 활용. 초록·리뷰·위키피디아·AI 요약은 일체 사용 금지.
   ↓ 변환 깨짐
   OCR recovery: 다운로드 PDF에 동일하게 적용
   ↓ OCR도 실패하거나 PDF 확보 불가
Layer 3 — 빈칸으로 둠
   해당 위키 섹션은 비워둠. 조작된 내용보다 빈칸이 낫습니다.
```

**Hard rules**:
- "(검증 대기)" 같은 caveat는 금지입니다. 지금 검증하거나 지금 삭제하십시오.
- Layer 건너뛰기 금지. 변환이 깨졌으면 먼저 OCR recovery를 시도하고, OCR도 실패할 때만 Layer 2로 넘어갑니다.
- JSTOR 헤더만 추출된 `.md` 변환본은 **Layer 1 성공이 아닙니다**.
- **어느 layer에서도 2차 출처는 금지**입니다. 리뷰·교과서·초록·위키피디아·Google Scholar 스니펫·AI 요약 모두 범주적으로 배제됩니다.
- Layer 2의 웹 접근은 오직 *논문 전체 PDF 확보*만을 위한 것입니다.
- Layer 2 다운로드는 별도 폴더(`papers_web/` + `papers_web/papers_web_md/`)에 저장합니다 — 감사 가능성과 출처 추적이 목적입니다.
- **OCR은 layer가 아니라 recovery step입니다.** 같은 PDF에서 텍스트 추출 방식만 바꿔 재시도하는 단계이며, 원전성(primary-source status)은 그대로 보존됩니다.

자세한 설명: [`docs/VERIFICATION_PROTOCOL.md`](docs/VERIFICATION_PROTOCOL.md).

---

## 12 Binding Rules

검증 프로토콜은 12개의 binding rules로 강제됩니다. Claude가 매 세션 시작 시 `CLAUDE.md`에서 자동 로드해 인제스트 중 hard check로 적용합니다. **소스 규율(1–6, 어떤 내용을 허용하는가)**과 **운영 규율(7–12, 어떻게 검증하고 자기 점검하는가)**로 묶입니다.

### 소스 규율 (1–6)

1. **소스 충실 요약**: 논문 안에 없는 내용은 쓰지 않습니다. 연결이 자명해 보여도 저자가 직접 쓰지 않은 한 작성 금지.
2. **3계층 검증 의무**: 로컬 1차 자료 → 웹 다운로드 1차 자료 PDF → 빈칸. 각 계층의 자료는 **전체를 읽어야** 합니다 — 초록만 읽기·skimming·snippet 요약은 검증이 아닙니다. 2차 자료(리뷰·초록·위키피디아·AI 요약)는 절대 금지.
3. **Don't write / Delete first** (두 시나리오): *신규 작성 시*에는 미검증 내용을 **아예 쓰지 않음**. *기존 편집 시*에는 미검증 내용을 **삭제**합니다 — `(검증 필요)` 같은 주석으로 보존하지 않습니다.
4. **위키에 있는 논문만 인용**: 본문 인용은 `references/`에 존재하는 파일을 가리켜야 합니다. `Smith_2010_ASR.md`가 없으면 먼저 인제스트하거나, 그 인용을 제거하십시오.
5. **공백을 즉흥으로 채우지 않음**: 위키에 해당 논문이 없으면 "X에 대한 논문이 없습니다 — PDF를 추가해 주세요"라고 보고합니다. 학습 데이터의 일반 지식으로 채우지 않습니다.
6. **Helpful 본능 차단**: "이 섹션이 빈약해 보인다"는 충동이 위반이 발생하기 직전의 신호입니다. 빈약한 게 정답.

### 운영 규율 (7–12)

7. **분량은 원칙이 아님**: 짧은 페이지는 정상이고, 긴 페이지는 경고 신호입니다. 소스가 뒷받침하는 만큼만 작성하십시오 — "빈약해 보인다"는 이유로 늘리지 마십시오.
8. **이진 plausibility 라벨 금지**: 미검증 내용에 "likely true"·"plausible"·"approximately X" 같은 라벨을 붙이지 마십시오. 검증(본문에 반영)하거나 삭제(빈칸 유지)합니다 — 회색 지대 자체가 실패 모드입니다.
9. **매 문장 자기 검문**: 매 문장마다 "이 안의 모든 사실이 검증되었는가?"를 자문합니다. 어느 한 주장(인용·데이터셋·표본·계수·귀속)이라도 불확실하면 그 문장 삭제.
10. **Layer 1 단편은 검증 아님**: JSTOR 헤더만·OCR 깨짐·워터마크만 있는 `.md` 변환은 Layer 1 성공이 **아닙니다**. Layer 2로 확장.
11. **인제스트 시 Verification Metadata 의무**: 모든 reference 페이지 끝에 어느 layer에서 검증됐는지 기록하는 Verification Metadata sub-section을 둡니다.
12. **검증 불가 = 빈칸, best-guess 아님**: 학습 데이터의 그럴듯함은 검증이 아닙니다.

운영 사례를 포함한 전체 설명: [`docs/ACCURACY_RULES.md`](docs/ACCURACY_RULES.md).

---

## 메모리 시스템

Claude Code 세션 사이에 영속하는 메모리 항목입니다. 다음 정보를 담습니다.

- **피드백 규칙**: 반복하지 말아야 할 본인의 정정 사항 (예: "미검증 인용 추가 금지", "research aim에 'task'라는 단어를 쓰지 말 것")
- **프로젝트 맥락**: 진행 중인 작업·마감일·결정 배경 (상대 날짜가 아닌 절대 날짜로 기록)
- **참조 정보**: 외부 시스템(Linear 프로젝트·Slack 채널·Grafana 대시보드 등)의 위치와 권위 영역

[`memory/examples/`](memory/examples/)에 예시 항목들이 들어 있습니다 — 각 항목은 rule + **Why** + **How to apply** 패턴을 따릅니다.

---

## 인덱스 — 위키의 척추

7개 master index 파일이 문헌 노트가 누적되면서 발생하는 drift를 방지:

- `index.md` — 카테고리별 프로젝트 상태
- `index_authors.md` — 모든 저자 알파벳순 (라틴 문자 + 비라틴 스크립트별 섹션)
- `index_detail.md` — 모든 개념·이론·방법 알파벳순
- `z_references_index.md` — 모든 reference 파일명 (중복 인제스트 방지)
- `z_ingest_history.md` — 프로젝트별 인제스트 타임스탬프 (증분 처리용)
- `log.md` — 운영 로그
- `books.md` — 도서 연대순

전체 스켈레톤: [`indexes/SKELETON_EXAMPLES.md`](indexes/SKELETON_EXAMPLES.md).

`z_*` 두 파일이 따로 존재하는 이유는 **작성 시점의 중복 제거(dedup-on-write)는 이미 늦기 때문**입니다. 내용이 미세하게 다른 `Smith_2010_ASR.md` 두 개가 일단 생겨버리면, 어느 쪽이 정본인지 흐려지고 두 버전이 따로 인용되면서 오류가 빠르게 누적됩니다.

---

## 스크립트

| 스크립트 | 목적 |
|----------|------|
| [`scripts/lint.py`](scripts/lint.py) | Wiki Lint — 11개 drift 점검 (고립된 reference, 학술지 연도 정렬, frontmatter 누락, 태그 표기 일관성, type 필드 일관성, 페이지 간 모순, 오래된 주장, prose→ref 자동 링크 후보, data gap 탐지 등) |
| [`scripts/autolink.py`](scripts/autolink.py) | 위키 내 다른 논문의 prose 멘션을 자동으로 마크다운 링크로 변환 (유일 매칭 안전망 포함) |
| [`scripts/index_papers.py`](scripts/index_papers.py) | 로컬 RAG 인덱서 (기본값: ChromaDB + bge-m3; 다른 도구로 교체 가능) |
| [`scripts/diag_ref2ref.py`](scripts/diag_ref2ref.py) | reference 간 링크 그래프 진단 |

설정 없이 동작합니다. 현재 폴더에서 상위로 거슬러 올라가 wiki 루트를 자동 감지하며, Windows·macOS·Linux 모두에서 작동합니다.

---

## RAG — 로컬 시맨틱 검색

위키에는 로컬 RAG 인덱서([`scripts/index_papers.py`](scripts/index_papers.py))가 함께 들어 있어 references·claims·concepts·projects·journals 전반을 시맨틱하게 검색할 수 있습니다. 모든 작업이 사용자 기기에서 일어나며, 외부 API를 호출하지 않고 데이터가 기기 밖으로 나가지 않습니다.

### 인덱싱 대상

- **기본**: `references/`, `claims/`, `general/`, `projects/`, `journals/`, 그리고 루트 인덱스 4개 (`index.md`, `index_authors.md`, `index_detail.md`, `books.md`).
- **제외**: `log.md`, `z_ingest_history.md`, `z_references_index.md` — 운영용 파일이라 시맨틱 검색에 노이즈입니다.
- **선택**: `papers/papers_md/`, `papers_web/papers_web_md/`의 원본 paper 변환본. `--include-raw` 플래그로만 활성화됩니다. 위키 카드 자체가 이미 source-faithful 요약이고, 원본 변환본까지 인덱싱하면 검색 노이즈와 임베딩 비용만 늘기 때문에 기본값은 비활성입니다.

### 저장 위치와 모델

- ChromaDB(SQLite 기반)가 `~/rag_db/chroma/`에 위치합니다. 위키 폴더 *바깥*이고 기기 로컬입니다. git이나 OneDrive로 동기화하지 않습니다 — 기기마다 자체적으로 인덱싱합니다.
- 임베딩 모델: `sentence-transformers`를 통한 `BAAI/bge-m3`. cross-file 256 chunk 배치, content-hash dedup, `max_seq_len=2048`로 attention 메모리 제한.
- DB는 파생 산출물입니다. 잃어버려도 `--full` 한 번 다시 돌리면 복구됩니다.

### 인덱싱 실행

```bash
python scripts/index_papers.py --incremental   # 마지막 실행 이후 변경된 파일만
python scripts/index_papers.py --full          # 전체 스캔 (full 안에서도 mtime 추적)
python scripts/index_papers.py --full --reset  # DB 와이프 + 처음부터 재구축
```

평소에는 `--incremental`이면 충분합니다. cold start 비용은 임베딩 모델 로드(~10–30초, 하드웨어에 따라 다름)이고, 그 이후엔 변경된 파일만 다시 임베딩합니다.

### 자동화

인덱싱은 **명시적으로 실행하도록 설계**되어 있습니다. 위키 자체가 진실의 단일 소스이고 인덱스는 그 위의 탐색용 캐시라는 비대칭을 워크플로가 강화해야 하기 때문입니다. 다만 매 인제스트마다 손으로 돌리는 건 번거롭습니다. 자동화 수준이 점점 높아지는 세 가지 패턴:

**Claude Code Stop hook (권장).** Claude Code 세션이 종료될 때마다 자동 재인덱싱. [`.claude/settings.json.example`](.claude/settings.json.example)을 `.claude/settings.json`으로 복사하면 활성화됩니다. Stop hook 파일은 gitignore되어 있어 기기마다 독립적으로 opt-in 가능합니다.

**백그라운드 작업 (일회성 비동기).** 같은 세션에서 작업을 이어가면서 인덱싱만 백그라운드로 돌리고 싶을 때:

```powershell
# PowerShell (Windows)
Start-Process -WindowStyle Hidden pwsh -ArgumentList "-c","python scripts/index_papers.py --incremental"
```

```bash
# Bash (Mac/Linux)
nohup python scripts/index_papers.py --incremental >/tmp/rag.log 2>&1 &
```

**스케줄 (Task Scheduler / cron).** 무인 상태로 주기적 재인덱싱. 대부분의 사용자에게는 과한 선택이지만, 여러 기기에서 인제스트하거나 watcher와 함께 운영할 때 robust한 선택입니다.

### 동시 실행 안전장치

`index_papers.py`는 파일 기반의 단일 writer lock(`~/rag_db/.index.lock`)을 사용합니다. 동일한 ChromaDB에 두 인덱서 프로세스가 동시에 write를 시도하면 SQLite 저장소가 손상될 수 있는데, 이 lock이 그것을 차단합니다. 다른 실행이 진행 중이면 깔끔하게 종료하고, 6시간 이상 묵은 lock(이전 실행이 죽으면서 남긴 것)은 자동으로 정리합니다. 덕분에 위의 백그라운드·Stop hook 패턴이 기본적으로 안전합니다 — Stop hook이 이전 작업이 끝나기 전에 다시 발동해도 두 번째 실행은 그냥 종료됩니다.

### 인덱스 조회

template은 인덱서만 포함하고 query client는 포함하지 않습니다. 두 가지 패턴:

1. **Python에서 ChromaDB 직접 접근** — `chromadb.PersistentClient(path="~/rag_db/chroma")`로 `research_wiki` 컬렉션을 쿼리합니다.
2. **DB 앞에 MCP 서버를 두기** — 컬렉션을 Claude Code의 도구로 노출시켜, RAG 검색을 대화 중 일반적인 tool call로 사용합니다.

어느 쪽이든 RAG가 돌려주는 것은 위키 페이지 경로입니다. **그 페이지를 열어 읽고 나서 인용하십시오.** RAG snippet은 탐색용일 뿐, 검증된 내용은 페이지 자체에 들어 있습니다. 페이지를 읽는 단계를 건너뛰는 것이 바로 12 binding rules가 막으려는 실패 양식입니다.

---

## 사회학 특화

기본 카테고리는 [ASA 섹션](https://www.asanet.org/communities-and-sections/sections/current-sections/)을 따릅니다.

- 토픽 7개: stratification, labor_markets, race_ethnicity, immigration, gender_family, political_sociology, education
- 횡단 카테고리 2개: methods, theory
- 지역·집단 연구 (예: asian_american, korean_society) — 토픽 축과 독립적

추적 대상 학술지 (인제스트 시 자동 등록):
- **사회학**: ASR, AJS, SF, ARS, Dem, RSSM, WO, IMR, JMF, GS, Socius, ESR, BJS, SSR, SMR/SM
- **인접 분야**: 경제학 상위 5대(AER, ECMA, JPE, QJE, REStud), 정치학 상위 5대(APSR, AJPS, JOP, BJPS, CPS), 심리학 상위 5대(ARP, PsychBull, PsychRev, JPSP, PsychSci)
- **한국 사회학**: 한국사회학, 경제와사회

본인 세부 전공에 맞게 자유롭게 조정할 수 있고, 그 외 구조는 분야 중립적입니다.

---

## 관련 시스템과의 비교

| 시스템 | 철학·관점 | 추가한 점 |
|--------|------------|----------|
| Karpathy LLM Wiki (2024) | "답변은 실제 논문에 닻을 내려야 한다." PDF → sources → wiki 3-tier 패턴을 개척. | 토대 |
| Ahrens (Smart Notes, 2017) | "영구 노트는 본인의 언어로." 연구자 본인의 아이디어 노트가 가치를 담는 층. | claims/ 레이어의 영감 |
| joonan30 adaptation (2025) | 응답 시점 4규칙(웹 검색 금지, 위키 우선 답변, 부족하면 PDF 재읽기, 없으면 없다고 답하기). | 응답 시점 규율 |
| **본 시스템** (2026) | 인제스트 시점의 정확성 + claims 레이어 + 사회학 scaffolding. | 3계층 검증·12 binding rules·5계층 위계 |

각 시스템의 상세는 위 표의 원본 publications와 repos를 참조하십시오.

---

## 다른 AI 에이전트와의 호환성

**Claude Code를 권장하지만, system prompt 파일을 지원하는 어떤 에이전트에서도 동작합니다.**

### AI 무관 (어디서나 그대로 작동)

- 위키 콘텐츠 자체 (plain markdown, Obsidian 호환)
- [`scripts/`](scripts/) 안의 모든 스크립트 — Python, AI 비의존
- 규율: 3계층 검증·12 binding rules·5계층 위계·source-only rule
- RAG 인덱서 ([`scripts/index_papers.py`](scripts/index_papers.py)) — 로컬 ChromaDB, 외부 API 호출 없음

### Claude 전용 부분 (다른 AI에선 등가물로 대체)

| Claude Code 기능 | 다른 에이전트의 등가물 |
|------------------|------------------------|
| `CLAUDE.md` (자동 로드되는 system prompt) | **OpenAI Codex CLI**: `AGENTS.md` (자동 로드) · **Cursor**: `.cursor/rules/*.mdc` 또는 `.cursorrules` · **Aider**: `CONVENTIONS.md` (`--read` 옵션) · **Continue**: `.continuerc.json`의 system prompt 필드 |
| `memory/` + `MEMORY.md` (세션 간 자동 누적) | 직접적 등가물 없음. 매 세션 `memory/*.md`를 system prompt에 inject하거나, 에이전트의 정적 rules 파일(Cursor Project Rules·Aider conventions 등)에 옮겨 넣어야 함 |
| `.claude/settings.json` Stop hook (세션 종료 시 자동 재인덱싱) | 대부분의 에이전트에 직접 등가물 없음. 대안: git `post-commit` hook·OS 파일 watcher(`watchdog`·PowerShell `Register-ObjectEvent`)·Task Scheduler·cron |

### 3단계 적응 절차 (예: Cursor·Codex CLI로 전환 시)

1. **System prompt 복사.** `cp CLAUDE.md AGENTS.md` (Codex) 또는 `cp CLAUDE.md .cursorrules` (Cursor). 일회성 작업이고, 이후엔 에이전트가 자동 로드합니다.
2. **메모리 처리 방식 결정.** (a) `memory/examples/*.md` 내용을 system prompt 파일 끝에 붙이기 또는 (b) 필요할 때만 on-demand 로드. 자동 누적 기능은 잃지만 교훈 자체는 보존됩니다 — 에이전트가 기록할 만한 실수를 할 때 수동으로 추가하시면 됩니다.
3. **Stop hook 대체.** `.git/hooks/post-commit`에 추가:
   ```bash
   python scripts/index_papers.py --incremental &
   ```
   `index_papers.py`의 lock guard가 동시 실행 안전을 보장합니다.

스크립트(`lint.py`·`autolink.py`·`index_papers.py`·`diag_ref2ref.py`)는 수정할 필요 없습니다.

### 주의 — 모델의 지시 준수도

규율은 글로 적혀 있지만, *그것을 따르는 정도*는 모델마다 다릅니다. 12 binding rules는 강한 자기억제("거짓 채움 금지, 빈칸이 정답")를 요구하는데, 모든 모델이 이를 동등하게 지키지는 않습니다:

- **Claude (Sonnet / Opus)** — 긴 지시 세트를 잘 따르고 자기억제 규칙 준수도가 높음. 본 시스템은 Claude를 기준으로 설계되었고, Claude에서 가장 자연스럽게 동작합니다.
- **GPT-4 / GPT-5 (Codex)** — tool use는 강하지만, 빈칸을 *일반 지식*으로 채우는 경향이 Claude보다 자주 나타납니다. 데이터셋 이름이나 표본 크기가 위조될 위험을 의식해야 합니다.
- **Gemini** — 긴 system prompt 준수도는 중간. tool use는 개선 중.
- **소형·로컬 모델 (GPT-OSS·Llama 계열 등)** — "검증 안 되면 빈칸으로" 같은 규칙을 따르기 어렵습니다. 인제스트 작업에는 권장하지 않고, 단순 검색 정도라면 무방.

**비-Claude 에이전트로 전환하기 전 권장 검증**: paper 한 편을 end-to-end로 인제스트해 보고, 에이전트가 (a) Layer 1 변환본 전체를 읽는지, (b) 검증되지 않은 sub-section을 빈채로 두는지, (c) 없는 인용을 지어내지 않는지 확인하십시오. 이 중 하나라도 실패하면, 그 에이전트가 다른 면에서 아무리 우수해도 본 워크플로엔 부적합한 신호입니다.

---

## 빠른 시작

**권장 경로**: [VS Code](https://code.visualstudio.com/)에 [Claude Code 확장](https://marketplace.visualstudio.com/items?itemName=Anthropic.claude-code)을 설치하고, 위키를 만들고 싶은 (빈) 폴더(예: `researchwiki` 같은 새 폴더 생성)를 워크스페이스로 연 다음, Claude Code 채팅 패널에 다음을 붙여 넣으십시오.

> "이 사회학 위키 템플릿을 사용해서 연구 위키를 셋업하려고 합니다: https://github.com/kchyhj/sociology-wiki-template
> clone부터 셋업까지 안내해 주세요 — 지금 열린 폴더에 repo를 clone하고, CLAUDE.md를 제 정보로 커스터마이즈하고, 폴더 스켈레톤을 만들어 주세요. 결정이 필요할 때마다 저에게 물어봐 주세요."

그러면 Claude가 template을 clone하고 repo의 지침을 읽은 뒤 본인의 이름·소속·카테고리·언어 정책 등을 묻고, 셋업 명령을 단계별로 확인받으며 실행합니다. 수동 CLI 작업 없이 한 세션 안에 본인 설정에 맞춰진 위키가 완성됩니다.

수동 셋업을 선호한다면 [`QUICKSTART.ko.md`](QUICKSTART.ko.md)에 동일한 단계가 직접 실행 가능한 명령으로 정리되어 있습니다.

---

## License

기본은 MIT 라이선스입니다. CC-BY-NC 등으로 바꾸려면 [`LICENSE`](LICENSE)를 편집하십시오.

이 시스템에서 다른 환경으로 이전 가능한(portable) 핵심은 구조적 패턴입니다. 구체적인 카테고리·스킬·도구는 커스터마이즈의 출발점일 뿐입니다.

---

## Acknowledgments

- Andrej Karpathy — 원형 LLM Wiki 패턴
- joonan30 — 연구 도메인으로의 generalization
- Sönke Ahrens — Smart Notes / Zettelkasten / permanent notes 패턴
- Andy Matuschak — evergreen notes 어휘
- Anthropic Claude Code 팀 — Skills + Memory 인프라

이 시스템은 한 연구자가 인용 환각(citation hallucination) 때문에 계속되는 오류를 방지하기 위해 여러 차례 재설계한 결과물입니다. 검증 프로토콜 부분은 다른 분야로도 옮겨갈 수 있는 portable한 부분입니다.
