// Android WebView에는 speechSynthesis가 없거나 한국어 음성이 없음 → 앱에서 대신 말해줌.
// loop.html의 speak()/speechSynthesis.cancel() 코드는 그대로 두고 이 파일이 대신 받아줌.
// 1) voice/index.json에 있는 문구는 미리 녹음한 음성(voice/*.m4a)을 재생
//    (Pleos 에뮬레이터에는 안드로이드 표준 TTS 엔진이 없어서 필요. tools/make-voice.py로 생성)
// 2) 녹음이 없는 문구는 안드로이드 TTS(window.AndroidTTS)로 넘김
(function(){
  if(!window.AndroidTTS)return; // 브라우저에서 열면 아무것도 안 함
  var clips=null,au=null;
  try{fetch('voice/index.json').then(function(r){return r.json()}).then(function(j){clips=j}).catch(function(){})}catch(e){}
  function stopClip(){if(au){try{au.pause()}catch(e){}au=null}}
  function U(t){this.text=t;this.lang='ko-KR';this.rate=1;this.voice=null}
  window.SpeechSynthesisUtterance=U;
  var ss={
    speak:function(u){
      var t=String(u.text||'').trim(),f=clips&&clips[t];
      stopClip();try{AndroidTTS.stop()}catch(e){}
      if(f){au=new Audio('voice/'+f);au.play().catch(function(){});return}
      try{AndroidTTS.speak(t,Number(u.rate||1))}catch(e){}
    },
    cancel:function(){stopClip();try{AndroidTTS.stop()}catch(e){}},
    getVoices:function(){return[{lang:'ko-KR',name:'Android'}]},
    onvoiceschanged:null,speaking:false,pending:false,paused:false
  };
  try{Object.defineProperty(window,'speechSynthesis',{value:ss,configurable:true})}catch(e){window.speechSynthesis=ss}
})();
