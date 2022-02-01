# ldap-filter Changelog

## 0.3.3

- Assert that NOT filters are closed by a parentheses

## 0.3.2

- Perform better checks for trailing characters
- Improve test coverage
- Change \*Filter.json to work recursively for child filters
- Bump assert-plus dependency to 1.0.0

## 0.3.1

- Tolerate underscores in attribute names

## 0.3.0

- Enforce stricter output escaping for buffer values
- **BREAKING** Rename `NotFilter.addfilter` to `NotFilter.setFilter`
- **BREAKING** Rewrite filter parser to be more strict about input.
  This _significantly_ changes the sort of filters which the parser files
  acceptable.  While the old parser would tolerate unescaped characters in
  the `()\*` set, the new parser requires them to be escaped via the `\XX`
  hex notation.  This is in keeping with
  [RFC 4514](http://tools.ietf.org/search/rfc4515)
- Perform better escaping for values which are not UTF-8

## 0.2.3
- Update dev dependencies
- Clean up asserts and prototypes

## 0.2.2

- Fix nested paren handling in parser

## 0.2.1

- Fix AndFilter per RFC4526

## 0.2.0

- Add 'attribute' accessor for ExtFilter matchType
- Improve API for custom match functions
- Support other value types in EqualityFilter

## 0.1.0

- Initial import from ldapjs
