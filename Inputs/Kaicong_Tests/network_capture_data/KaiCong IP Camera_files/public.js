function monitorDetail()
{
   window.open("http://kaicong.cc/forum.php?mod=viewthread&tid=39631")
}
function deviceStatus()
{
   window.open("http://kaicong.cc/forum.php?mod=viewthread&tid=39632")
}
function TimerDetail()
{
   window.open("http://kaicong.cc/forum.php?mod=viewthread&tid=39633")
}
function MultiDevice()
{
   window.open("http://kaicong.cc/forum.php?mod=viewthread&tid=39634")
}
function ipDetail()
{
   window.open("http://kaicong.cc/forum.php?mod=viewthread&tid=39635")
}
function Wireless()
{
   window.open("http://kaicong.cc/forum.php?mod=viewthread&tid=39636")
}
function EmailDetail()
{
   window.open("http://kaicong.cc/forum.php?mod=viewthread&tid=39637")
}
function AlarmDetail()
{
   window.open("http://kaicong.cc/forum.php?mod=viewthread&tid=39639")
}
function UpgradeDetail()
{
   window.open("http://kaicong.cc/forum.php?mod=viewthread&tid=39641")
}
function FTPDetail()
{
   window.open("http://kaicong.cc/forum.php?mod=viewthread&tid=39641")
}
function RecordVideo()
{
   window.open("http://kaicong.cc/forum.php?mod=viewthread&tid=39640")
}

function getcookie(name)
{
	var strCookie=document.cookie;
  var arrCookie=strCookie.split('; ');
  for (var i=0;i<arrCookie.length;i++)
  {
		var arr=arrCookie[i].split('=');
    if (arr[0]==name)
			return unescape(arr[1]);
  }
  return '';
}
function setcookie(name,value,expirehours)
{
	var cookieString=name+'='+escape(value);
  if (expirehours>0)
  {
		var date=new Date();
    date.setTime(date.getTime()+expirehours*3600*1000);
    cookieString=cookieString+'; expires='+date.toGMTString();
	}
  document.cookie=cookieString;
}

function setDocTitle(name)
{
	top.document.title = name;
}


var language=getcookie('language');
   if (language==''){
	
 	language='simple_chinese';
		if (navigator.appName == 'Netscape') 
				language = navigator.language; 
		else 
				language = navigator.browserLanguage; 
		if (language.indexOf('zh-cn') > -1) 
			language = 'simple_chinese'; 
		else if (language.indexOf('zh-tw') > -1) 
			language = 'traditional_chinese'; 
		else if (language.indexOf('es') > -1) 
			language = 'spanish'; 
		else if (language.indexOf('fr') > -1) 
			language = 'french'; 
		else if (language.indexOf('ru') > -1) 
			language = 'russian'; 
		else if (language.indexOf('pl') > -1) 
			language = 'polski'; 
		else if (language.indexOf('it') > -1) 
			language = 'italian'; 
		else if (language.indexOf('pt') > -1) 
			language = 'Portuguese'; 
		else if (language.indexOf('de') > -1) 
			language = 'deutsch'; 	
		else if (language.indexOf('po') > -1) 
			language = 'portugal';  
		else  
			language = 'english';  
}
if (language=='simple_chinese')
	document.write('<script src="simple_chinese/string.js"><\/script><script src="simple_chinese/oem.js"><\/script>');
else if (language=='traditional_chinese')	
	document.write('<script src = "traditional_chinese/string.js"><\/script><script src = "traditional_chinese/oem.js"><\/script>');
else if (language=='spanish')
	document.write('<script src="spanish/string.js"><\/script><script src="spanish/oem.js"><\/script>');
else if (language=='french')
	document.write('<script src="french/string.js"><\/script><script src="french/oem.js"><\/script>');
else if (language=='russian')
	document.write('<script src="russian/string.js"><\/script><script src="russian/oem.js"><\/script>');
else if (language=='polski')
	document.write('<script src="polski/string.js"><\/script><script src="polski/oem.js"><\/script>');
else if (language=='italian')
	document.write('<script src="italian/string.js"><\/script><script src="italian/oem.js"><\/script>');
else if (language=='deutsch')
	document.write('<script src="deutsch/string.js"><\/script><script src="deutsch/oem.js"><\/script>');
else if (language=='portugal')
	document.write('<script src="portugal/string.js"><\/script><script src="portugal/oem.js"><\/script>');
else
	document.write('<script src="english/string.js"><\/script><script src="english/oem.js"><\/script>');
	
function reboot()
{
	var url;
	if (confirm(str_sure_reboot))
	{
		top.reboot_seconds = 30;
		url='reboot.cgi?next_url=reboot.htm';
		url+='&loginuse='+top.cookieuser+'&loginpas='+top.cookiepass;
		//$.getScript(url);
		location=url;
	}
}
function restore_factory()
{
	var url;
	if (confirm(str_sure_restore))
	{
		top.reboot_seconds = 30;
		url='restore_factory.cgi?next_url=rebootme.htm';
		url+='&loginuse='+top.cookieuser+'&loginpas='+top.cookiepass;
		//$.getScript(url);
		location=url;
	}
}
function gobackpage()
{
	//alert(top.goback_page);
	location=top.goback_page;
}
function removeSelfClass(){
	$("#dd-status", parent.document).removeClass("selected");
	$("#dd-alias", parent.document).removeClass("selected");
	$("#dd-datetime", parent.document).removeClass("selected");
	//$("#dd-media", parent.document).removeClass("selected");
	$("#dd-recordpath", parent.document).removeClass("selected");
	
	$("#dd-alarm", parent.document).removeClass("selected");
	$("#dd-mail", parent.document).removeClass("selected");
	$("#dd-ftp", parent.document).removeClass("selected");
	$("#dd-log", parent.document).removeClass("selected");
	
	$("#dd-ip", parent.document).removeClass("selected");
	$("#dd-ap", parent.document).removeClass("selected");
	$("#dd-wireless", parent.document).removeClass("selected");
	$("#dd-ddns", parent.document).removeClass("selected");
	
	
	$("#dd-ptz", parent.document).removeClass("selected");
	
	$("#dd-multidev", parent.document).removeClass("selected");
	$("#dd-user", parent.document).removeClass("selected");
	$("#dd-upgrade", parent.document).removeClass("selected");

}
