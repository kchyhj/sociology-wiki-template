# 빠른 시작 (Quickstart)

10분이면 위키가 작동합니다. 영어 원본: [`QUICKSTART.md`](QUICKSTART.md).

---

## 권장 경로: VS Code + Claude Code

가장 쉬운 시작 방법은 **[VS Code](https://code.visualstudio.com/)에 [Claude Code 확장](https://marketplace.visualstudio.com/items?itemName=Anthropic.claude-code)을 설치한 뒤**, **위키를 만들고 싶은 (빈) 폴더(예: `researchwiki` 같은 새 폴더 생성)를 워크스페이스로 열고** **채팅 패널에서 Claude에게 셋업을 부탁하는 것**입니다.

이렇게 시작해 보십시오:

> "이 사회학 위키 템플릿을 사용해서 연구 위키를 셋업하려고 합니다: https://github.com/kchyhj/sociology-wiki-template
> clone부터 셋업까지 안내해 주세요 — 지금 열린 폴더에 repo를 clone하고, CLAUDE.md를 제 정보로 커스터마이즈하고, 폴더 스켈레톤을 만들어 주세요. 결정이 필요할 때마다 저에게 물어봐 주세요."

그러면 Claude가 template을 clone하고 repo의 지침을 읽은 뒤 이름·소속·카테고리·언어 정책을 묻고, 폴더 생성 명령을 실행하며, 각 단계를 적용하기 전에 확인을 받습니다. 수동 CLI 작업 없이도 본인 설정에 맞춰진 위키가 첫 세션 안에 완성됩니다. 아래 셋업 절차는 *참고용*이며, Claude에게 맡기면 대화로 처리해 줍니다.

수동으로 직접 진행하려는 경우, 아래 명령들도 그대로 사용 가능합니다.

---

## 사전 준비

- **VS Code**(권장) + **Claude Code 확장** — 또는 본인이 선호하는 Claude Code 환경 (CLI·desktop)
- **Python 3.10+** (3.12 권장)
- **Git**
- **Obsidian** (무료, 브라우징용 — 강력 권장; 다른 markdown 에디터도 작동)

Python 패키지 (한 번만 설치):
```bash
pip install pymupdf4llm chromadb sentence-transformers
```

이는 번들 스크립트가 사용하는 **default**입니다. 동등한 alternatives도 작동 — 자유롭게 교체 가능:

| Default | Alternatives |
|---|---|
| `pymupdf4llm` (PDF→markdown 변환) | `pdfplumber`, `pdfminer.six`, MinerU, Marker, GROBID |
| `ocrmypdf` (스캔본·이미지 PDF용 OCR recovery) | `pytesseract` 직접 호출, `marker`, MinerU, Apple Preview OCR, ABBYY FineReader |
| `chromadb` (로컬 vector store) | `lancedb`, `qdrant`, `weaviate`, FAISS |
| `BAAI/bge-m3` (embedding 모델) | `bge-large`, `e5-large`, `nomic-embed`, OpenAI/Cohere embeddings |
| `Obsidian` (markdown viewer) | VS Code, Typora, Foam, Logseq |
| `Zotero` (reference manager) | Mendeley, Paperpile, JabRef |

구조적 commitment (5계층 위계·3계층 검증·source-only 규칙·연구자 본인의 아이디어 노트(atomic claims))는 도구 선택에 *의존하지 않음*. 도구를 바꿔도 규칙은 그대로 유지.

---

## 셋업

### Step 1: 템플릿 clone 또는 복사

```bash
git clone https://github.com/YOUR-USERNAME/sociology-wiki-template my-wiki
cd my-wiki

# 본인 git repo로 초기화
rm -rf .git
git init
```

### Step 2: CLAUDE.md 커스터마이즈

위키 루트의 `CLAUDE.md`를 열어 placeholder를 치환:

- `YOUR-NAME` → 본인 handle 또는 이름
- `YOUR-INSTITUTION` → 소속
- `YOUR-CATEGORIES` → 본인이 작업하는 primary 토픽 카테고리
- `YOUR-WIKI-PATH` → 위키 폴더의 절대 경로

선택 조정:
- **Language Policy** 섹션 — (A) English-only, (B) 단일 비영어 언어, (C) **본인 언어 + English mirror** 중 하나 선택. 자세한 내용은 CLAUDE.md → Language Policy
- **Tracked Journals** — field-specific 학술지 추가
- **Categories** — 본인 sub-discipline에 맞게 기본 7개 조정

### Step 3: 폴더 스켈레톤 생성

```bash
mkdir -p papers/papers_md papers_web/papers_web_md references claims projects
mkdir -p general/{stratification,labor_markets,race_ethnicity,immigration,gender_family,political_sociology,education,methods,theory}
mkdir -p journals/{Econ,PolSci,Psych}
touch papers/.gitkeep papers/papers_md/.gitkeep papers_web/.gitkeep papers_web/papers_web_md/.gitkeep references/.gitkeep claims/.gitkeep projects/.gitkeep
```

(이 명령은 bash brace expansion을 사용합니다. Windows에서는 Git Bash나 WSL에서 실행하십시오. PowerShell 사용자는 폴더를 수동으로 만들거나 `New-Item` 루프를 작성해야 합니다. 또는 권장 경로인 VS Code + Claude Code로 Claude에게 셋업을 맡기는 것이 가장 간편합니다.)

### Step 4: Root 인덱스 파일 생성

빈 stub으로 시작:

```bash
touch index.md index_authors.md index_detail.md
touch z_references_index.md z_ingest_history.md
touch books.md log.md
```

각 파일의 채워진 모습은 [`indexes/SKELETON_EXAMPLES.md`](indexes/SKELETON_EXAMPLES.md) 참조.

### Step 5: 카테고리 랜딩 페이지 생성

각 `general/{category}/` 에 `0_index.md` 생성 (`templates/category_0_index.md` 사용):

```bash
for cat in stratification labor_markets race_ethnicity immigration gender_family political_sociology education methods theory; do
  cp templates/category_0_index.md general/$cat/0_index.md
done
```

각 `0_index.md`를 편집해 카테고리명·한 줄 설명 입력.

### Step 6: Claims hub 생성

```bash
cp templates/claim.md claims/example_claim.md  # 첫 claim placeholder
```

`claims/0_index.md` 생성 — status 섹션 포함 (Confident / Working / Retired).

### Step 7: Obsidian 셋업 (선택)

1. Obsidian을 실행합니다.
2. **Open folder as Vault**로 위키 폴더를 엽니다.
3. Obsidian이 폴더를 인덱싱하며 backlinks, graph view, 검색이 즉시 작동합니다.

Obsidian은 파일을 수정하지 않습니다 — 실제 편집은 Claude Code가 맡고, Obsidian은 렌더링과 탐색을 담당합니다.

---

## 인제스트 워크플로 — 한 논문을 위키에 추가하기

가장 자주 하게 되는 작업입니다. 한 번 익히면 매번 같은 절차로 반복됩니다.

### Step A: 기존 요약 확인

먼저 `z_references_index.md`에서 파일명 stem을 grep합니다. 이미 존재하면 *다시 작성하지 마십시오*. `projects:` 리스트만 업데이트하면 됩니다.

```bash
grep "Smith_2020_ASR" z_references_index.md
```

### Step B: PDF를 `papers/`에 배치

```bash
cp ~/Downloads/some_paper.pdf papers/Smith_2020_ASR.pdf
```

파일명 규칙은 `{성}_{연도}_{학술지약어}.md` 형식을 따릅니다.
- 단독 저자: `Smith_2020_ASR.md`
- 두 저자: `Smith_Jones_2020_ASR.md`
- 3인 이상 저자: `Smith_etal_2020_ASR.md`
- 도서: `Author_2015_BookTitle.md`
- 비라틴 문자 논문: 원어 표기 사용 (예: `김저자_2024_한국학술지.md`)

### Step C: PDF → markdown 변환

```bash
python -c "
import pymupdf4llm
md = pymupdf4llm.to_markdown('papers/Smith_2020_ASR.pdf')
open('papers/papers_md/Smith_2020_ASR.md','w',encoding='utf-8').write(md)
"
```

### Step D: Layer 1 검증 — 변환 상태 점검

이 단계가 *가장 자주 건너뛰게 되는* 단계입니다. 빠르지만 결정적입니다.

```bash
wc -l papers/papers_md/Smith_2020_ASR.md         # 500-3000 줄 정도 예상
head -50 papers/papers_md/Smith_2020_ASR.md      # 첫 50줄이 introduction 본문인지 확인
grep -c "^## " papers/papers_md/Smith_2020_ASR.md # 섹션 헤더 5-15개 정도 예상
```

**변환이 깨졌다면**(JSTOR 헤더만 추출되거나, OCR이 비어 있거나, 문자가 scramble된 경우, 본문이 비어 있는 경우 — 스캔본·이미지 기반 PDF에서 흔함):

먼저 **OCR recovery**를 같은 PDF에 시도합니다 (Layer 1 안에서의 재시도):

```bash
# ocrmypdf: tesseract 기반 오픈소스; 기본 권장 OCR 도구
ocrmypdf papers/Smith_2020_ASR.pdf papers/Smith_2020_ASR.ocr.pdf
python -c "
import pymupdf4llm
md = pymupdf4llm.to_markdown('papers/Smith_2020_ASR.ocr.pdf')
open('papers/papers_md/Smith_2020_ASR.md','w',encoding='utf-8').write(md)
"
```

대안 도구: `marker`·`MinerU`(표·수식 강함, 정량 사회학 논문에 유리), Apple Preview(macOS 단발 처리).

OCR 결과를 다시 점검(wc/head/grep). 정상이면 Layer 1 성공 — Verification Metadata에 `via OCR (ocrmypdf)` 표기. OCR마저 garbage라면 Layer 1 사용 불가 → **Step E (Layer 2)로 escalate**.

**변환이 처음부터 정상이라면** 곧바로 Step F로 진행합니다.

### Step E: Layer 2 — 웹에서 논문 PDF 다운로드

Layer 1이 불가능할 때만 진행합니다. **웹에서는 *논문 자체의 PDF만* 찾으십시오.** abstract·리뷰·위키피디아는 금지입니다.

탐색 순서:
1. 저자의 institutional website
2. preprint server (SSRN, NBER, IZA, arXiv, OSF, PsyArXiv)
3. ResearchGate, Academia.edu (저자 허가 하에 호스팅된 경우)
4. 학술지의 open-access 버전
5. institutional library access

다운로드 이후:

```bash
cp ~/Downloads/Smith_2020_ASR.pdf papers_web/Smith_2020_ASR.pdf

python -c "
import pymupdf4llm
md = pymupdf4llm.to_markdown('papers_web/Smith_2020_ASR.pdf')
open('papers_web/papers_web_md/Smith_2020_ASR.md','w',encoding='utf-8').write(md)
"
```

웹에서 받은 PDF도 스캔본일 수 있으므로 변환을 다시 점검(wc/head/grep)합니다. 변환이 깨졌으면 Layer 1과 동일한 패턴으로 **OCR recovery**를 시도합니다:

```bash
ocrmypdf papers_web/Smith_2020_ASR.pdf papers_web/Smith_2020_ASR.ocr.pdf
python -c "
import pymupdf4llm
md = pymupdf4llm.to_markdown('papers_web/Smith_2020_ASR.ocr.pdf')
open('papers_web/papers_web_md/Smith_2020_ASR.md','w',encoding='utf-8').write(md)
"
```

OCR 결과까지 정상이면 `papers_web/papers_web_md/Smith_2020_ASR.md`를 Layer 1과 동일하게 읽습니다. Verification Metadata에 URL·다운로드 날짜와 함께 `via OCR (ocrmypdf)` 표기.

**Layer 2도 실패한 경우**(PDF 확보 불가 또는 OCR도 garbage) → Layer 3 = **해당 sub-section을 빈칸으로 두십시오**. 2차 출처로 대체하지 마십시오.

### Step F: 본문 읽기

`papers/papers_md/Smith_2020_ASR.md` 또는 `papers_web/papers_web_md/Smith_2020_ASR.md`를 *전체* 읽습니다. 다음 항목을 정리합니다.
- 서지 정보 (저자·연도·학술지·권·호·페이지) — 본문이 명시한 메타데이터를 *그대로*
- 데이터셋 이름 — 정확하게 (NLSY79 ≠ NLSY97, ECLS-K ≠ ELS)
- 표본 크기 — 정확한 수치로
- 방법 — 구체적인 식별 전략까지
- 핵심 발견 + 구체적 수치 + 해당 table·figure 번호

### Step G: `references/{stem}.md` 작성

`templates/reference_paper.md`(논문) 또는 `templates/reference_book.md`(도서)를 복사한 뒤 다음 sub-section들을 채웁니다.

- **Frontmatter** (year·authors·journal·themes·projects·theories)
- **Bibliography** 줄
- **Topic** — 무엇을 연구하고 왜 중요한지 2~3 문장으로
- **Key Theory / Framework** — 이론들을 *어떻게 적용*했는지 (단순 나열이 아님)
- **Data & Methods** — 데이터·방법·식별 전략을 단계별로
- **Key Findings** — 6~10개의 발견을 sub-section 헤더로 정리. 각각 구체적 수치 + 메커니즘 해석 + 조건부 발견 + robustness + 이론적 함의를 포함
- **Relevance to This Project** — 본인의 해석이 허용되는 *유일한* 섹션
- **Scholarly Conversation** — 다른 위키 references와의 타입화된 관계(선행·확장·대안·비판·재현·경계 사례)
- **Verification Metadata** — 어떤 Layer를 사용했는지 기록 (날짜·URL·버전 등)

**원전 충실 규칙을 적용하십시오**: 논문이 말하지 않은 내용은 적지 마십시오. 검증되지 않은 sub-section은 빈칸으로 둡니다.

### Step H: Side 파일 업데이트

```
z_references_index.md     ← 항목 추가: Smith_2020_ASR.md | theme:Stratification | projects:[your_project]
journals/ASR.md          ← 항목 추가 (최신 연도 상단)
general/{category}/0_index.md ← "Key Literature" 섹션에 추가
index_authors.md         ← 저자 알파벳 위치에 삽입
index_detail.md          ← 새 이론·개념·방법 알파벳순 추가
```

3+ 인제스트 논문이 한 이론을 공유하면: `general/{category}/{theory}.md` 개념 페이지 생성·업데이트.

### Step I: 로그 기록

`log.md`에 한 줄:

```markdown
## [YYYY-MM-DD] ingest | Smith_2020_ASR
- new theories: [list]
- new concept page: (있다면)
- journals/ASR.md updated
```

### Step J: Git commit

```bash
git add -A
git commit -m "Ingest: Smith 2020 ASR"
```

### 인제스트 디시플린 — 핵심 규칙

- **한 논문씩 완전 수렴**: 다음 인제스트를 시작하기 전에 현재 작업을 완전히 마무리합니다. (12 binding rules의 일부는 아니지만 운영상 권장 패턴 — 일괄 인제스트는 검증 깊이를 떨어뜨립니다.)
- **빈 섹션은 정상**: 검증되지 않은 sub-section은 빈칸으로 둡니다.
- **인용 검증**: 본문에서 다른 논문을 언급할 때는 `references/`에 그 파일이 있는지 확인한 뒤 마크다운 링크로 연결합니다.
- **수치는 정확하게**: "약 50%" 같은 표현은 금지입니다. 정확한 숫자를 적거나 빈칸으로 둡니다.
- **방법 귀속**: 논문이 "fixed effects"라고 명시하지 않았다면 적지 마십시오.

전체 인제스트 절차 상세는 [`docs/WORKFLOWS.md`](docs/WORKFLOWS.md)의 "Ingest a New Paper" 섹션을 참조하십시오.

---

## Claim 작성

대화 중 본인이 *여러 논문을 합성한 입장*을 말하면 Claude가 "claim 노트로 저장할까요?"라고 제안합니다. 승인 시 다음 절차를 따릅니다.

1. **인용 검증** — 인용된 모든 reference가 `references/`에 실제로 존재하는지 확인합니다.
2. **상태(status) 결정** — `working`(잠정) / `confident`(검증·활용 완료) / `retired`(후속 증거로 폐기) 중 하나를 선택합니다.
3. **파일명** — 내용을 설명하는 snake_case 슬러그 (예: `kr_edu_premium_cohort_divergence.md`).
4. **본문 작성** — `templates/claim.md`를 사용합니다. 불릿이 아닌 **산문(prose)**으로, 한두 단락 분량으로 적습니다.
5. **반대 증거 섹션 필수** — 한계와 반대 증거를 정직하게 기재합니다.
6. **`claims/0_index.md` 갱신** — 활성 claim 목록에 추가합니다.
7. **로그 기록**.

자세한 절차는 [`docs/WORKFLOWS.md`](docs/WORKFLOWS.md)의 "File a Claim" 섹션을 참조하십시오.

---

## 린트 워크플로 — 위키 drift 점검

**언제 실행하는가**: 인제스트가 일정 분량 누적된 시점, 새 프로젝트를 시작할 때, 또는 GitHub에 push하기 전.

```bash
python scripts/lint.py
```

### Lint가 점검하는 11개 항목

| Step | 점검 |
|------|------|
| 1 | **프로젝트 폴더 유효성** — `projects/{year}/{name}/`이 실제 연구 폴더에 대응하는지 |
| 2 | **Orphan references** — 모든 `references/*.md`가 `z_references_index.md`에 등록되고 최소 1개 프로젝트의 `references.md`에서 참조되는지 |
| 3 | **학술지 연도 정렬** — 각 `journals/*.md`의 연도가 내림차순인지 |
| 4 | **인덱스 동기화** — `references/` 디렉토리와 `z_references_index.md`가 일치하는지 |
| 5 | **Frontmatter 커버리지** — 모든 reference 페이지가 YAML frontmatter 보유 |
| 6 | **태그 표기 drift** — `#theme/*`와 `#journal/*`이 일관된 casing (CamelCase 또는 snake_case, 한쪽) |
| 7 | **Type 필드 일관성** — `book_chapter` vs `book-chapter` drift 없음 |
| 8 | **교차 페이지 모순** — 같은 논문이 다른 페이지에서 모순되게 묘사되는지 |
| 9 | **Stale "recent research" 주장** — 카테고리 페이지가 5+ 년 된 논문을 "최근"으로 칭하는지 |
| 10 | **Ref→ref link audit** — 다른 위키 논문의 prose 멘션이 markdown-linked 되어야 함 (`scripts/autolink.py`로 자동) |
| 11 | **Data gap 탐지** — 프로젝트 bibliographies에서 3+회 인용됐으나 미인제스트 논문 |

### Lint 출력

스크립트는 발견 사항을 구조적 보고서 형태로 출력합니다. 각 항목별로 다음 정보를 보여줍니다.
- 해당 파일 경로
- 구체적인 issue
- 자동 수정 가능 여부

### 안전한 자동 수정

다음 항목들은 lint가 자동으로 적용합니다.
- **태그 표기 정규화** (예: `#theme/stratification` → `#theme/Stratification`)
- **Type 필드 통일** (예: `book_chapter` → `book-chapter`)
- **학술지 연도 정렬** (내림차순으로 재정렬)

### 수동 수정이 필요한 경우

- **교차 페이지 모순** — 어느 버전이 원전과 일치하는지 판단한 뒤 하나로 통일합니다.
- **오래된 주장** — 어느 후속 논문이 그 주장을 대체했는지 판단해 내용을 갱신합니다.
- **Data gap** — 인제스트 여부를 본인이 결정합니다.

### Lint 이후 처리

수정 사항을 커밋한 뒤 push합니다.

```bash
git -C wiki add -A
git -C wiki commit -m "Wiki lint YYYY-MM-DD: {핵심 변경 요약}"
git -C wiki push
```

로그를 기록합니다.

```markdown
## [YYYY-MM-DD] lint | wiki-wide
- 오래된 주장 N건 수정
- 고립된 reference N건 식별
- prose 멘션 N건 자동 링크화 (Step 10)
- data gap 후보 N건 flag
```

### Autolink 단독 실행

대규모 인제스트 직후 reference 간 링크를 갱신할 때 사용합니다.

```bash
python scripts/autolink.py --dry    # 미리보기
python scripts/autolink.py          # 적용
```

유일 매칭(unique-match)이 아닌 모호한 경우(예: Card 2001 *ILRR* + Card 2001 *JLE*)는 자동으로 처리되지 않고 flag만 표시됩니다.

자세한 절차는 [`docs/WORKFLOWS.md`](docs/WORKFLOWS.md)의 "Run Wiki Lint" 섹션을 참조하십시오.

---

## RAG 인덱싱

위키 콘텐츠를 로컬 벡터 DB에 인덱싱해 cross-paper 검색이 가능해지도록 합니다.

### 첫 인덱싱 (전체)

```bash
python scripts/index_papers.py --full
```

- 첫 실행에서는 references·general·claims·projects·journals 폴더와 root의 4개 인덱스 파일을 모두 처리합니다.
- 소요 시간은 위키 크기에 비례합니다(수백 파일 기준 십수 분에서 수십 분).

### 증분 인덱싱 (이후 매번)

```bash
python scripts/index_papers.py --incremental
```

- 파일 mtime을 기준으로 변경된 파일만 처리합니다.
- 일반적으로 수 초 이내에 끝납니다.

### 언제 재인덱싱하나

- 인제스트가 어느 정도 누적된 시점
- Lint sweep 이후(여러 파일이 수정된 직후)
- 대규모 리팩토링 직후

DB는 `~/rag_db/chroma/`에 저장됩니다 (위키 폴더 바깥, 기기 로컬 — git이나 OneDrive로 동기화하지 않음). `~/rag_db/.index.lock`의 단일 writer lock이 두 인덱서 프로세스가 동시에 같은 DB를 손상시키는 것을 막습니다.

### 자동 재인덱싱

매번 손으로 돌리는 게 번거롭다면 자동화 옵션이 셋 있습니다.

**Claude Code Stop hook (권장).** [`.claude/settings.json.example`](.claude/settings.json.example)을 `.claude/settings.json`으로 복사하면 Claude Code 세션이 끝날 때마다 자동으로 incremental 재인덱싱이 돕니다. `.claude/settings.json`은 gitignore되어 있어서 기기마다 독립적으로 opt-in 가능합니다.

**백그라운드 작업 (일회성 비동기).** 같은 세션에서 작업을 이어가면서 인덱싱만 백그라운드로 돌리고 싶을 때:

```powershell
# PowerShell (Windows)
Start-Process -WindowStyle Hidden pwsh -ArgumentList "-c","python scripts/index_papers.py --incremental"
```

```bash
# Bash (Mac/Linux)
nohup python scripts/index_papers.py --incremental >/tmp/rag.log 2>&1 &
```

**Task Scheduler / cron.** 무인 상태로 주기적으로 돌리는 방식. 대부분의 사용자에게는 과한 선택이나, 여러 기기·watcher와 함께 운영할 때 가장 robust합니다.

### Claude Code에서 검색 사용

위키 내 cross-paper 검색이 활성화되면 Claude는 `search_papers` MCP 도구로 위키를 조회합니다. *단, RAG 검색 결과 자체는 인용이 아닙니다* — 정확성을 위해 검색에서 나온 페이지를 항상 *직접 read 도구로 확인*하십시오.

자세한 인덱싱 범위·모델 설정·query 패턴은 [`README.ko.md`의 "RAG — 로컬 시맨틱 검색" 섹션](README.ko.md#rag--로컬-시맨틱-검색)을 참조하십시오.

---

## 일상 워크플로

셋업 이후 일반적인 세션은 다음과 같이 진행됩니다.

1. 위키 폴더에서 Claude Code를 실행합니다.
2. Claude가 자동으로 `CLAUDE.md`를 읽습니다.
3. 사용자가 요청합니다: "다음 PDF를 인제스트: `~/Downloads/new_paper.pdf`".
4. Claude가 인제스트 워크플로를 실행합니다(앞서 본 Step A~J).
5. 사용자는 Obsidian에서 source markdown을 함께 확인합니다.
6. Claude가 `references/{stem}.md`를 작성합니다 (원전 충실 규칙).
7. 사용자가 spot-check하고 필요한 경우 정정을 요청합니다.
8. side 파일들이 갱신됩니다.
9. 로그가 기록됩니다.
10. 커밋합니다.

한 논문당 소요 시간은 본인의 페이스에 따라 달라집니다. *느리게 가는 것이 이 시스템이 받아들이는 트레이드오프*입니다.

---

## 처음에는 건너뛰어도 되는 것

시작 단계에서는 다음을 미뤄도 됩니다.

- **`scripts/autolink.py`는 references가 어느 정도 쌓인 뒤에 실행하십시오** — 그 전에는 link할 대상이 없습니다.
- **카테고리 narrative 섹션(History of Debates·Recent Themes)은 해당 카테고리에 references가 충분히 쌓인 후 작성하십시오.**
- **개념 페이지는 같은 개념을 공유하는 references가 충분히 쌓인 후 만드십시오.**
- **하루에 너무 많은 인제스트를 하지 마십시오.** 논문당 완전 수렴(per-paper convergence)이 throughput보다 중요합니다.

천천히 쌓는 것이 핵심입니다. 규율이 속도보다 우선합니다.

---

## 문제가 생겼을 때

| 문제 | 해결 |
|------|------|
| 변환본이 깨짐 (JSTOR header만 추출됨) | Layer 1 사용 불가로 처리하고 Verification Metadata에 기록한 뒤 Layer 2로 escalate |
| 파일명 충돌 (기존 파일이 존재) | `z_references_index.md`를 확인하고, 기존 파일에 프로젝트 태그만 추가하십시오. 다시 쓰지 마십시오 |
| 고치고 싶지 않은 drift를 lint가 보고 | `log.md`에 명시적 예외와 이유를 함께 기록 |
| Claude가 논문에 없는 내용을 작성하려 함 | 중지하십시오. 원전 충실 규칙입니다. 빈 섹션이 올바른 상태입니다 |
| Obsidian에 파일이 보이지 않음 | Obsidian을 새로고침하고 파일이 실제로 저장되었는지 확인 |
| RAG가 결과를 반환하지 않음 | `scripts/index_papers.py --rebuild-history`를 시도하고 필요하면 reindex |

---

## 더 깊이

첫 5-10편 후:
- [`PHILOSOPHY.ko.md`](PHILOSOPHY.ko.md) — *왜* 이 규칙들이 존재하는지
- [`docs/VERIFICATION_PROTOCOL.md`](docs/VERIFICATION_PROTOCOL.md) — 중심 규율
- [`docs/WORKFLOWS.md`](docs/WORKFLOWS.md) — 전체 절차 목록
- Claude의 행동을 정정해 가며 메모리 항목(`memory/MEMORY.md`)을 누적

문헌이 어느 정도 쌓인 뒤(50편 안팎)에는 다음을 본격화합니다.
- claim 작성 (Layer 3)
- 정기적인 lint 실행
- 개념 페이지 구축
- 카테고리 간 cross-link

문헌이 더 누적되면(200편 안팎):
- 위키가 실제 연구 자산으로 작동하기 시작합니다.
- RAG가 유의미한 검색 결과를 반환합니다.
- Cross-paper 합성이 자연스러워집니다.
- claim 누적이 본인의 연구 voice를 형성합니다.

---

## License & Attribution

본 템플릿은 MIT 라이선스를 따릅니다. 자유롭게 변형해 사용하십시오. 다른 환경으로 옮길 수 있는(portable) 핵심은 정확성 규율과 5계층 위계이고, 그 외의 구체적 요소는 사회학 영역에 특화된 장식입니다.

본인이 발전시킨 결과를 공유할 때 attribution은 환영하지만 필수는 아닙니다.
