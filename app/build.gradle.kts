plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.loop.pleos"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.loop.pleos"
        minSdk = 28
        targetSdk = 35
        versionCode = 1
        versionName = "1.0.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            // 공모전 제출용: 디버그 키로 서명(별도 키스토어 없이 설치 가능한 APK)
            signingConfig = signingConfigs.getByName("debug")
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
    androidResources {
        // 자산(jpg/json/svg)을 압축하지 않고 그대로 넣음
        noCompress += listOf("jpg", "png", "webp", "json", "svg", "woff2", "ttf")
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.appcompat:appcompat:1.7.0")
    implementation("androidx.webkit:webkit:1.12.1")
}
