// Android WebView에는 speechSynthesis가 없거나 한국어 음성이 없음 → 안드로이드 TTS(window.AndroidTTS)로 연결.
// loop.html의 speak()/speechSynthesis.cancel() 코드는 그대로 두고 이 파일이 대신 받아줌.
(function(){
  if(!window.AndroidTTS)return; // 브라우저에서 열면 아무것도 안 함
  function U(t){this.text=t;this.lang='ko-KR';this.rate=1;this.voice=null}
  window.SpeechSynthesisUtterance=U;
  var ss={
    speak:function(u){try{AndroidTTS.speak(String(u.text||''),Number(u.rate||1))}catch(e){}},
    cancel:function(){try{AndroidTTS.stop()}catch(e){}},
    getVoices:function(){return[{lang:'ko-KR',name:'Android'}]},
    onvoiceschanged:null,speaking:false,pending:false,paused:false
  };
  try{Object.defineProperty(window,'speechSynthesis',{value:ss,configurable:true})}catch(e){window.speechSynthesis=ss}
})();
