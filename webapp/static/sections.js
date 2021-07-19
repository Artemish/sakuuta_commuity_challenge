var data = null;

fetch("/sections/" + section_id + "/as_json")
  .then(response => response.json())
  .then(d => data = d);

function createState() {
  function initializeState() {
    state = this;

    fetch("/sections/" + section_id + "/as_json")
      .then(response => response.json())
      .then(function(data) {
        state.sectionData = data;
        state.loading = false;
        state.jp_text = Object.values(data.jp_text);
        state.en_text = Object.values(data.en_text);
        state.speaker = Object.values(data.speaker);
        state.isTranslated = Object.values(data.translated);
        state.translatedText = state.en_text[0];
        state.startIndex = parseInt(Object.keys(data.en_text)[0]);
        state.totalLines = state.jp_text.length;
      });
  }

  function nextUntranslated() {
    while ((this.index < (this.totalLines - 1)) && (this.isTranslated[this.index])) {
      this.index += 1;
    }

    this.translatedText = this.en_text[this.index];
  }

  function nextTranslated() {
    while ((this.index < (this.totalLines - 1)) && (!this.isTranslated[this.index])) {
      this.index += 1;
    }

    this.translatedText = this.en_text[this.index];
  }

  function nextLine() {
    if (this.index < (this.totalLines - 1)) {
      this.index += 1;
    }

    this.translatedText = this.en_text[this.index];
  }

  function prevLine() {
    if (this.index > 0) {
      this.index -= 1;
    }

    this.translatedText = this.en_text[this.index];
  }

  function translateLine() {
    var lineNo = this.index + this.startIndex;
    var state = this;

    var config = {
      method: "POST",
      body: state.translatedText,
    };

    console.log(config);

    fetch('/translate/' + lineNo, config).then(
      function (result) { 
        state.en_text[state.index] = config.body;
        state.isTranslated[state.index] = true;
      }
    );
  }

  return {
    'section_id': section_id,
    'loading': true,
    'index': 0,
    'startIndex': 0,
    'sectionData': {},
    'en_text': [null],
    'jp_text': [null],
    'speaker': [null],
    'translatedText': "",
    'totalLines': 0,
    'initializeState': initializeState,
    'nextLine': nextLine,
    'prevLine': prevLine,
    'nextUntranslated': nextUntranslated,
    'nextTranslated': nextTranslated,
    'isTranslated': [],
    'translateLine': translateLine,
  }
}
