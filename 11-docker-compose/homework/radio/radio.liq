# Параметры для подключения к Icecast
icecast_host = "icecast"
icecast_port = 8000
icecast_password = "hackme"

# Создаем источник тишины
silent_source = blank()

# Указываем источник из локальной директории с mp3 файлами
#playlist_1 = playlist("/music/playlist.m3u", reload_mode="watch")
#radio = mksafe(playlist_1)

# Настройка трансляции в Icecast
output.icecast(
  %vorbis,
  host = icecast_host,
  port = icecast_port,
  password = icecast_password,
  mount = "/silent.ogg",
  name = "Silence test stream",
  description = "If you don't hear anything, then it's okay",
  silent_source
)

#output.icecast(
#  %vorbis,
#  host = icecast_host,
#  port = icecast_port,
#  password = icecast_password,
#  mount = "/radio.ogg",
#  name = "My radio",
#  description = "Non-stop best music in the world",
#  radio
#)
