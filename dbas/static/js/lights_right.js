var Ovr2b='';
if(typeof document.compatMode!='undefined'&&document.compatMode!='BackCompat')
  cot_t2_DOCtp="_top:expression(document.documentElement.scrollTop+document.documentElement.clientHeight-this.clientHeight);" +
	  " _left:expression(document.documentElement.scrollLeft  +  document.documentElement.clientWidth  -  offsetWidth);}";
else
  cot_t2_DOCtp="_top:expression(document.body.scrollTop+document.body.clientHeight-this.clientHeight);" +
	  " _left:expression(document.body.scrollLeft  +  document.body.clientWidth  -  offsetWidth);}";

if(typeof document.compatMode!='undefined'&&document.compatMode!='BackCompat')
	cot_t2_DOCtp2="_top:expression(document.documentElement.scrollTop-20+document.documentElement.clientHeight-this.clientHeight);}";
else
	cot_t2_DOCtp2="_top:expression(document.body.scrollTop-20+document.body.clientHeight-this.clientHeight);}";
var cot_tl4_bodyCSS='* html {background: fixed;background-repeat: repeat;background-position: right top;}',
	cot_tl4_fixedCSS='#cot_tl4_fixed{position:fixed; _position:absolute; top:0px; right:0px; clip:rect(0 100 85 0);' + cot_t2_DOCtp,
	cot_tl4_popCSS='#cot_tl4_pop {background-color: transparent; position:fixed; _position:absolute; height:1920px; width: 98px; right:' +
    ' 120px; bottom: 20px; overflow: hidden; visibility: hidden; z-index: 100;' + cot_t2_DOCtp2;

document.write('<style type="text/css">'+cot_tl4_bodyCSS+cot_tl4_fixedCSS+cot_tl4_popCSS+'</style>');

function COT(cot_tl4_theLogo,cot_tl4_LogoType,LogoPosition,theAffiliate)
{document.write('<div id="cot_tl4_fixed">');
document.write('<><img src='+cot_tl4_theLogo+' alt="" border="0"></a>');
document.write('</div>');}

//if(window.location.protocol == "http:")
COT("http://tester2.synthasite.com/resources/flashing%20christmas%20lights%20right.gif", "SC2", "none");