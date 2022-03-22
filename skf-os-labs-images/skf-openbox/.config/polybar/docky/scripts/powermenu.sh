#!/usr/bin/env bash

## Author  : Aditya Shakya
## Mail    : adi1090x@gmail.com
## Github  : @adi1090x
## Twitter : @adi1090x

dir="~/.config/polybar/docky/scripts/rofi"
uptime=$(uptime -p | sed -e 's/up //g')

rofi_command="rofi -theme $dir/powermenu.rasi"

# Options
skfsite="- SKF Main website"
skfchat="- SKF Chat channel"
writeups="- SKF Lab Write-ups"
cheatsheet="- OWASP Cheat Sheet Series"
wstg="- OWASP Web Security Testing Guide"

# Variable passed to rofi
options="$skfsite\n$skfchat\n$writeups\n$cheatsheet\n$wstg"

chosen="$(echo -e "$options" | $rofi_command -p "   Uptime Lab: $uptime" -dmenu -selected-row 0)"
case $chosen in
    $skfsite)
		firefox --new-tab https://www.securityknowledgeframework.org &
    ;;
    $writeups)
		firefox --new-tab https://owasp-skf.gitbook.io/asvs-write-ups/ &
    ;;
    $skfchat)
		firefox --new-tab https://gitter.im/Security-Knowledge-Framework/Lobby &
    ;;
    $cheatsheet)
		firefox --new-tab https://cheatsheetseries.owasp.org/Glossary.html &
    ;;
    $wstg)
		firefox --new-tab https://owasp.org/www-project-web-security-testing-guide/stable/ &
    ;;
esac
