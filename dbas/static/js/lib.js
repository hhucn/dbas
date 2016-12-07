/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */


/**
 * Swaps the element with the parameter
 * @param from element
 * @param to element
 * @returns {*}
 */
function swapElements (from, to) {
    const copy_to = $(to).clone(true),
	    copy_from = $(from).clone(true);
	$(to).replaceWith(copy_from);
	$(from).replaceWith(copy_to);
}


/**
 * Src: http://stackoverflow.com/questions/11919065/sort-an-array-by-the-levenshtein-distance-with-best-performance-in-javascript
 * @param s1
 * @param s2
 */
function levensthein (s1, s2){
	let row2=[];
	if (s1 === s2) {
		return 0;
	} else {
		const s1_len = s1.length, s2_len = s2.length;
		if (s1_len && s2_len) {
			let i1 = 0, i2 = 0, a, b, c, c2, row = row2;
			while (i1 < s1_len)
				row[i1] = ++i1;
			while (i2 < s2_len) {
				c2 = s2.charCodeAt(i2);
				a = i2;
				++i2;
				b = i2;
				for (i1 = 0; i1 < s1_len; ++i1) {
					c = a + (s1.charCodeAt(i1) === c2 ? 0 : 1);
					a = row[i1];
					b = b < a ? (b < c ? b + 1 : c) : (a < c ? a + 1 : c);
					row[i1] = b;
				}
			}
			return b;
		} else {
			return s1_len + s2_len;
		}
	}
}
