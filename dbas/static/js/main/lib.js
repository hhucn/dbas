/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

/**
 * Src: http://stackoverflow.com/questions/11919065/sort-an-array-by-the-levenshtein-distance-with-best-performance-in-javascript
 * @param s1
 * @param s2
 */
function levensthein(s1, s2) {
    'use strict';

    var rowTwo = [];
    if (s1 === s2) {
        return 0;
    } else {
        var s1Len = s1.length, s2Len = s2.length;
        if (s1Len && s2Len) {
            var i1 = 0, i2 = 0, a, b, c, c2, row = rowTwo;
            while (i1 < s1Len) {
                ++i1;
                row[i1] = i1;
            }
            while (i2 < s2Len) {
                c2 = s2.charCodeAt(i2);
                a = i2;
                ++i2;
                b = i2;
                for (i1 = 0; i1 < s1Len; ++i1) {
                    c = a + (s1.charCodeAt(i1) === c2 ? 0 : 1);
                    a = row[i1];
                    if (b < a) {
                        b = b < c ? b + 1 : c;
                    } else {
                        b = a < c ? a + 1 : c;
                    }
                    row[i1] = b;
                }
            }
            return b;
        } else {
            return s1Len + s2Len;
        }
    }
}
