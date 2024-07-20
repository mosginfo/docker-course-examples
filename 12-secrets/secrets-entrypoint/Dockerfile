FROM php:8.3-apache

# Копируем из вспомогательного образа
# все необходимые библиотеки и скрипты/программы
COPY --from=kyzimaspb/useful \
    /apps/compver/compver.sh \
    /apps/secrets/secrets.sh \
    /usr/local/bin/

COPY ./ /

# Затираем входную точку из образа PHP пользовательской,
# в которой выполняем дополнительные проверки перед запуском web/fast-cgi сервера
ENTRYPOINT ["docker-entrypoint.sh"]
# Если инструкция ENTRYPOINT была указана, то CMD обнуляется автоматически
# Восстанавливаем значение из родительского образа
CMD ["apache2-foreground"]
