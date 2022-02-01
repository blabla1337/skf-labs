'use strict';

var fs = require('fs');
var UnicodeTrie = require('unicode-trie');

var categories=["Cc","Zs","Po","Sc","Ps","Pe","Sm","Pd","Nd","Lu","Sk","Pc","Ll","So","Lo","Pi","Cf","No","Pf","Lt","Lm","Mn","Me","Mc","Nl","Zl","Zp","Cs","Co"];var combiningClasses=["Not_Reordered","Above","Above_Right","Below","Attached_Above_Right","Attached_Below","Overlay","Iota_Subscript","Double_Below","Double_Above","Below_Right","Above_Left","CCC10","CCC11","CCC12","CCC13","CCC14","CCC15","CCC16","CCC17","CCC18","CCC19","CCC20","CCC21","CCC22","CCC23","CCC24","CCC25","CCC30","CCC31","CCC32","CCC27","CCC28","CCC29","CCC33","CCC34","CCC35","CCC36","Nukta","Virama","CCC84","CCC91","CCC103","CCC107","CCC118","CCC122","CCC129","CCC130","CCC132","Attached_Above","Below_Left","Left","Kana_Voicing","CCC26","Right"];var scripts=["Common","Latin","Bopomofo","Inherited","Greek","Coptic","Cyrillic","Armenian","Hebrew","Arabic","Syriac","Thaana","Nko","Samaritan","Mandaic","Devanagari","Bengali","Gurmukhi","Gujarati","Oriya","Tamil","Telugu","Kannada","Malayalam","Sinhala","Thai","Lao","Tibetan","Myanmar","Georgian","Hangul","Ethiopic","Cherokee","Canadian_Aboriginal","Ogham","Runic","Tagalog","Hanunoo","Buhid","Tagbanwa","Khmer","Mongolian","Limbu","Tai_Le","New_Tai_Lue","Buginese","Tai_Tham","Balinese","Sundanese","Batak","Lepcha","Ol_Chiki","Braille","Glagolitic","Tifinagh","Han","Hiragana","Katakana","Yi","Lisu","Vai","Bamum","Syloti_Nagri","Phags_Pa","Saurashtra","Kayah_Li","Rejang","Javanese","Cham","Tai_Viet","Meetei_Mayek","null","Linear_B","Lycian","Carian","Old_Italic","Gothic","Old_Permic","Ugaritic","Old_Persian","Deseret","Shavian","Osmanya","Osage","Elbasan","Caucasian_Albanian","Linear_A","Cypriot","Imperial_Aramaic","Palmyrene","Nabataean","Hatran","Phoenician","Lydian","Meroitic_Hieroglyphs","Meroitic_Cursive","Kharoshthi","Old_South_Arabian","Old_North_Arabian","Manichaean","Avestan","Inscriptional_Parthian","Inscriptional_Pahlavi","Psalter_Pahlavi","Old_Turkic","Old_Hungarian","Hanifi_Rohingya","Old_Sogdian","Sogdian","Elymaic","Brahmi","Kaithi","Sora_Sompeng","Chakma","Mahajani","Sharada","Khojki","Multani","Khudawadi","Grantha","Newa","Tirhuta","Siddham","Modi","Takri","Ahom","Dogra","Warang_Citi","Nandinagari","Zanabazar_Square","Soyombo","Pau_Cin_Hau","Bhaiksuki","Marchen","Masaram_Gondi","Gunjala_Gondi","Makasar","Cuneiform","Egyptian_Hieroglyphs","Anatolian_Hieroglyphs","Mro","Bassa_Vah","Pahawh_Hmong","Medefaidrin","Miao","Tangut","Nushu","Duployan","SignWriting","Nyiakeng_Puachue_Hmong","Wancho","Mende_Kikakui","Adlam"];var eaw=["N","Na","A","W","H","F"];var data = {categories:categories,combiningClasses:combiningClasses,scripts:scripts,eaw:eaw};

var log2 = Math.log2 || (n => Math.log(n) / Math.LN2);

var bits = n => log2(n) + 1 | 0;

var buildUnicodeProperties = (data, trie) => {
  // compute the number of bits stored for each field
  var CATEGORY_BITS = bits(data.categories.length - 1);
  var COMBINING_BITS = bits(data.combiningClasses.length - 1);
  var SCRIPT_BITS = bits(data.scripts.length - 1);
  var EAW_BITS = bits(data.eaw.length - 1);
  var NUMBER_BITS = 10; // compute shift and mask values for each field

  var CATEGORY_SHIFT = COMBINING_BITS + SCRIPT_BITS + EAW_BITS + NUMBER_BITS;
  var COMBINING_SHIFT = SCRIPT_BITS + EAW_BITS + NUMBER_BITS;
  var SCRIPT_SHIFT = EAW_BITS + NUMBER_BITS;
  var EAW_SHIFT = NUMBER_BITS;
  var CATEGORY_MASK = (1 << CATEGORY_BITS) - 1;
  var COMBINING_MASK = (1 << COMBINING_BITS) - 1;
  var SCRIPT_MASK = (1 << SCRIPT_BITS) - 1;
  var EAW_MASK = (1 << EAW_BITS) - 1;
  var NUMBER_MASK = (1 << NUMBER_BITS) - 1;

  var getCategory = codePoint => {
    var val = trie.get(codePoint);
    return data.categories[val >> CATEGORY_SHIFT & CATEGORY_MASK];
  };

  var getCombiningClass = codePoint => {
    var val = trie.get(codePoint);
    return data.combiningClasses[val >> COMBINING_SHIFT & COMBINING_MASK];
  };

  var getScript = codePoint => {
    var val = trie.get(codePoint);
    return data.scripts[val >> SCRIPT_SHIFT & SCRIPT_MASK];
  };

  var getEastAsianWidth = codePoint => {
    var val = trie.get(codePoint);
    return data.eaw[val >> EAW_SHIFT & EAW_MASK];
  };

  var getNumericValue = codePoint => {
    var val = trie.get(codePoint);
    var num = val & NUMBER_MASK;

    if (num === 0) {
      return null;
    } else if (num <= 50) {
      return num - 1;
    } else if (num < 0x1e0) {
      var numerator = (num >> 4) - 12;
      var denominator = (num & 0xf) + 1;
      return numerator / denominator;
    } else if (num < 0x300) {
      val = (num >> 5) - 14;
      var exp = (num & 0x1f) + 2;

      while (exp > 0) {
        val *= 10;
        exp--;
      }

      return val;
    } else {
      val = (num >> 2) - 0xbf;

      var _exp = (num & 3) + 1;

      while (_exp > 0) {
        val *= 60;
        _exp--;
      }

      return val;
    }
  };

  var isAlphabetic = codePoint => {
    var category = getCategory(codePoint);
    return category === 'Lu' || category === 'Ll' || category === 'Lt' || category === 'Lm' || category === 'Lo' || category === 'Nl';
  };

  var isDigit = codePoint => getCategory(codePoint) === 'Nd';

  var isPunctuation = codePoint => {
    var category = getCategory(codePoint);
    return category === 'Pc' || category === 'Pd' || category === 'Pe' || category === 'Pf' || category === 'Pi' || category === 'Po' || category === 'Ps';
  };

  var isLowerCase = codePoint => {
    return getCategory(codePoint) === 'Ll';
  };

  var isUpperCase = codePoint => getCategory(codePoint) === 'Lu';

  var isTitleCase = codePoint => getCategory(codePoint) === 'Lt';

  var isWhiteSpace = codePoint => {
    var category = getCategory(codePoint);
    return category === 'Zs' || category === 'Zl' || category === 'Zp';
  };

  var isBaseForm = codePoint => {
    var category = getCategory(codePoint);
    return category === 'Nd' || category === 'No' || category === 'Nl' || category === 'Lu' || category === 'Ll' || category === 'Lt' || category === 'Lm' || category === 'Lo' || category === 'Me' || category === 'Mc';
  };

  var isMark = codePoint => {
    var category = getCategory(codePoint);
    return category === 'Mn' || category === 'Me' || category === 'Mc';
  };

  return {
    getCategory,
    getCombiningClass,
    getScript,
    getEastAsianWidth,
    getNumericValue,
    isAlphabetic,
    isDigit,
    isPunctuation,
    isLowerCase,
    isUpperCase,
    isTitleCase,
    isWhiteSpace,
    isBaseForm,
    isMark
  };
};

var trie = new UnicodeTrie(fs.readFileSync(__dirname + '/data.trie'));
var unicodeProperties = buildUnicodeProperties(data, trie);

module.exports = unicodeProperties;
//# sourceMappingURL=unicode-properties.cjs.js.map
