# নকশা — compact NEXUS

ডিফল্ট একটি ছোট voice orb: visible mic state, সাম্প্রতিক কথা/উত্তর, Stop/mute/settings ও text fallback। Detailed transcript dialog এবং বড় workspace চাইলে আলাদা করে খোলা যায়। CSS pulse/level bars হালকা; idle-এ continuous canvas/render loop নেই।

Microphone permission-এর পরে bounded turn capture, CPU ASR, session-scoped durable task, approved command অথবা প্রকৃত model response, তারপর local speech। Playback চলার সময় mic বন্ধ; generation counters পুরোনো input/result ফিরে session শুরু হতে দেয় না।

মেমোরির স্তর: চলমান কথোপকথন, SQLite-এ স্থায়ী তথ্য, সূত্রসহ imported knowledge ও feedback। সীমিত প্রাসঙ্গিক তথ্য context-এ যায়; model weights নিজে বদলায় না। কাজের completed steps persisted; অনিশ্চিত side effect review ছাড়া replay হয় না।

Windows C launcher ও bundled Python UI আগে খোলে, models background-এ প্রস্তুত হয়। Single-instance lock ও private localhost token নিজের session নিয়ন্ত্রণ করে। Unsupported capability ও service failure স্পষ্ট থাকে। API key ছাড়া local CPU default; public web hosting, AGI, সব কাজে সাফল্য বা commercial-game play দাবি নেই।
