package com.loop.pleos

import android.content.Context
import android.speech.tts.TextToSpeech
import android.webkit.JavascriptInterface
import java.util.Locale

/** JS에서 window.AndroidTTS.speak(text, rate) / stop() 으로 호출 (assets/tts-shim.js). */
class TtsBridge(context: Context) : TextToSpeech.OnInitListener {
    private val tts = TextToSpeech(context.applicationContext, this)
    @Volatile private var ready = false
    private var pending: Pair<String, Float>? = null

    override fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) {
            tts.language = Locale.KOREAN
            ready = true
            pending?.let { speak(it.first, it.second.toDouble()) }
            pending = null
        }
    }

    @JavascriptInterface
    fun speak(text: String, rate: Double) {
        val r = rate.toFloat().coerceIn(0.5f, 2f)
        if (!ready) { pending = text to r; return }
        tts.setSpeechRate(r)
        tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, "loop")
    }

    @JavascriptInterface
    fun stop() { if (ready) tts.stop() }

    fun shutdown() { tts.stop(); tts.shutdown() }
}
