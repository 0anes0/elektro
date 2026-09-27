"""Testler sistem diline ve kullanıcı ayarına bağlı olmasın: her zaman İngilizce."""

import os
import tempfile

os.environ["ELEKTRO_LANG"] = "en"
os.environ["XDG_CONFIG_HOME"] = tempfile.mkdtemp(prefix="elektro-test-")
