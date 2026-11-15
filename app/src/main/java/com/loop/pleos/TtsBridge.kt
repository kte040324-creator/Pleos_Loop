package com.loop.pleos

import android.content.Context
import android.speech.tts.TextToSpeech
import android.util.Log
import android.webkit.JavascriptInterface
import ai.pleos.playground.tts.constant.ErrorType
import ai.pleos.playground.tts.constant.Mode
import ai.pleos.playground.tts.listener.EventListener
import ai.pleos.playground.tts.listener.OnInitializeListener
import java.util.Locale
import ai.pleos.playground.tts.TextToSpeech as PleosTts

/**
 * JS에서 window.AndroidTTS.speak(text, rate) / stop() 으로 호출 (assets/tts-shim.js).
 * 1) Pleos 차량: Pleos Connect SDK의 TextToSpeech(온디바이스)로 말한다.
 * 2) 그 외 기기: 안드로이드 표준 TextToSpeech로 말한다.
 */
class TtsBridge(context: Context) : TextToSpeech.OnInitListener {
    private val ctx = context.applicationContext
    private var tts: TextToSpeech? = null
    @Volatile private var ready = false
    private var pending: Pair<String, Float>? = null

    private var pleos: PleosTts? = null
    @Volatile private var pleosReady = false

    init {
        try {
            pleos = PleosTts(ctx, Mode.ON_DEVICE).also { p ->
                p.initialize(object : OnInitializeListener {
                    override fun onSuccess() {
                        Log.i(TAG, "Pleos TTS ready")
                        runCatching { p.setLocale(Locale.KOREA) }
                        p.addEventListener(object : EventListener {
                            override fun onStart() { Log.i(TAG, "Pleos TTS start") }
                            override fun onReady() {}
                            override fun onDone() { Log.i(TAG, "Pleos TTS done") }
                            override fun onError(e: ErrorType) { Log.w(TAG, "Pleos TTS error: $e") }
                            override fun onStop() {}
                            override fun onUpdatedRms(rms: Double) {}
                        })
                        pleosReady = true
                        pending?.let { speak(it.first, it.second.toDouble()) }; pending = null
                    }
                    override fun onFailure(e: ErrorType) { Log.w(TAG, "Pleos TTS init failed: $e") }
                })
            }
        } catch (e: Throwable) { Log.w(TAG, "Pleos TTS unavailable: $e") }
        tts = TextToSpeech(ctx, this)
    }

    override fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) {
            tts?.language = Locale.KOREAN
            ready = true
            if (!pleosReady) { pending?.let { speak(it.first, it.second.toDouble()) }; pending = null }
        }
    }

    /** Pleos TTS를 쓸 수 있으면 true (tts-shim.js가 미리 녹음한 음성 대신 이걸 씀) */
    @JavascriptInterface
    fun isPleos(): Boolean = pleosReady

    @JavascriptInterface
    fun speak(text: String, rate: Double) {
        val r = rate.toFloat().coerceIn(0.5f, 2f)
        val p = pleos
        if (pleosReady && p != null) {
            try { p.speak(text, true); return } catch (e: Throwable) { Log.w(TAG, "Pleos speak failed: $e") }
        }
        if (!ready) { pending = text to r; return }
        tts?.setSpeechRate(r)
        tts?.speak(text, TextToSpeech.QUEUE_FLUSH, null, "loop")
    }

    @JavascriptInterface
    fun stop() {
        if (pleosReady) runCatching { pleos?.stop() }
        if (ready) tts?.stop()
    }

    fun shutdown() {
        runCatching { pleos?.stop(); pleos?.release() }
        tts?.stop(); tts?.shutdown()
    }

    private companion object { const val TAG = "LoopTTS" }
}
