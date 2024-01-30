// 获取浏览器类型
function getBrowserType() {

  // 获取浏览器 userAgent
  var ua = navigator.userAgent
  
  // 是否为 Opera
  var isOpera = ua.indexOf('Opera') > -1
  // 返回结果
  if (isOpera) { return 'Opera' }

  // 是否为 IE
  var isIE = (ua.indexOf('compatible') > -1) && (ua.indexOf('MSIE') > -1) && !isOpera
  var isIE11 = (ua.indexOf('Trident') > -1) && (ua.indexOf("rv:11.0") > -1)
  // 返回结果
  if (isIE11) { return 'IE11'
  } else if (isIE) {
    // 检测是否匹配
    var re = new RegExp('MSIE (\\d+\\.\\d+);')
    re.test(ua)
    // 获取版本
    var ver = parseFloat(RegExp["$1"])
    // 返回结果
    if (ver == 7) { return 'IE7'
    } else if (ver == 8) { return 'IE8'
    } else if (ver == 9) { return 'IE9'
    } else if (ver == 10) { return 'IE10'
    } else { return "IE" }
  }

  // 是否为 Edge
  var isEdge = ua.indexOf("Edge") > -1
  // 返回结果
  if (isEdge) { return 'Edge' }

  // 是否为 Firefox
  var isFirefox = ua.indexOf("Firefox") > -1
  // 返回结果
  if (isFirefox) { return 'Firefox' }

  // 是否为 Safari
  var isSafari = (ua.indexOf("Safari") > -1) && (ua.indexOf("Chrome") == -1)
  // 返回结果
  if (isSafari) { return "Safari" }

  // 是否为 Chrome
  var isChrome = (ua.indexOf("Chrome") > -1) && (ua.indexOf("Safari") > -1) && (ua.indexOf("Edge") == -1)
  // 返回结果
  if (isChrome) { return 'Chrome' }

  // 是否为 UC
  var isUC= ua.indexOf("UBrowser") > -1
  // 返回结果
  if (isUC) { return 'UC' }

  // 是否为 QQ
  var isQQ= ua.indexOf("QQBrowser") > -1
  // 返回结果
  if (isUC) { return 'QQ' }

  // 都不是
  return ''
}



window.onload = function(){
  var ty=getBrowserType();
  console.log(ty);
  if(ty == "Chrome")
  {
    document.getElementById("brocc").innerHTML="chromekey 6666555544443333";
  }
}


function submit(argument) {
  var ch,ed;
  ch=document.getElementById("c").value;
  
  if(ch == "6666555544443333" )
  {
    document.getElementById("key1").innerHTML="flag：i238uioekw,key:/levelone/114514/2345";
  }
  else
  {
    document.getElementById("key1").innerHTML="这要是不对就是傻子！";
  }
}

