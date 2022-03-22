#!/usr/bin/env bash

# Color files
PFILE="$HOME/.config/polybar/docky/colors.ini"
RFILE="$HOME/.config/polybar/docky/scripts/rofi/colors.rasi"

# Change colors
change_color() {
	# polybar
	sed -i -e 's/background = #.*/background = #1F1F1F/g' $PFILE
	sed -i -e 's/foreground = #.*/foreground = #FFFFFF/g' $PFILE
	sed -i -e 's/foreground-alt = #.*/foreground-alt = #8F8F8F/g' $PFILE
	sed -i -e "s/module-fg = #.*/module-fg = $MF/g" $PFILE
	sed -i -e "s/primary = #.*/primary = $AC/g" $PFILE
	sed -i -e 's/secondary = #.*/secondary = #E53935/g' $PFILE
	sed -i -e 's/alternate = #.*/alternate = #7cb342/g' $PFILE
	
	# rofi
	cat > $RFILE <<- EOF
	/* colors */

	* {
	  al:   #00000000;
	  bg:   #1F1F1FFF;
	  bga:  ${AC}33;
	  bar:  ${MF}FF;
	  fg:   #FFFFFFFF;
	  ac:   ${AC}FF;
	}
	EOF
	
	polybar-msg cmd restart
}

if  [[ $1 = "--amber" ]]; then
	MF="#1F1F1F"
	AC="#ffb300"
	change_color
elif  [[ $1 = "--blue" ]]; then
	MF="#FFFFFF"
	AC="#1e88e5"
	change_color
elif  [[ $1 = "--blue-gray" ]]; then
	MF="#FFFFFF"
	AC="#546e7a"
	change_color
elif  [[ $1 = "--brown" ]]; then
	MF="#FFFFFF"
	AC="#6d4c41"
	change_color
elif  [[ $1 = "--cyan" ]]; then
	MF="#1F1F1F"
	AC="#00acc1"
	change_color
elif  [[ $1 = "--deep-orange" ]]; then
	MF="#FFFFFF"
	AC="#f4511e"
	change_color
elif  [[ $1 = "--deep-purple" ]]; then
	MF="#FFFFFF"
	AC="#5e35b1"
	change_color
elif  [[ $1 = "--green" ]]; then
	MF="#FFFFFF"
	AC="#43a047"
	change_color
elif  [[ $1 = "--gray" ]]; then
	MF="#FFFFFF"
	AC="#757575"
	change_color
elif  [[ $1 = "--indigo" ]]; then
	MF="#FFFFFF"
	AC="#3949ab"
	change_color
elif  [[ $1 = "--light-blue" ]]; then
	MF="#1F1F1F"
	AC="#039be5"
	change_color
elif  [[ $1 = "--light-green" ]]; then
	MF="#1F1F1F"
	AC="#7cb342"
	change_color
elif  [[ $1 = "--lime" ]]; then
	MF="#1F1F1F"
	AC="#c0ca33"
	change_color
elif  [[ $1 = "--orange" ]]; then
	MF="#1F1F1F"
	AC="#fb8c00"
	change_color
elif  [[ $1 = "--pink" ]]; then
	MF="#FFFFFF"
	AC="#d81b60"
	change_color
elif  [[ $1 = "--purple" ]]; then
	MF="#FFFFFF"
	AC="#8e24aa"
	change_color
elif  [[ $1 = "--red" ]]; then
	MF="#FFFFFF"
	AC="#e53935"
	change_color
elif  [[ $1 = "--teal" ]]; then
	MF="#FFFFFF"
	AC="#00897b"
	change_color
elif  [[ $1 = "--yellow" ]]; then
	MF="#1F1F1F"
	AC="#fdd835"
	change_color
else
	cat <<- _EOF_
	No option specified, Available options:
	--amber	--blue		--blue-gray	--brown
	--cyan	--deep-orange	--deep-purple	--green
	--gray	--indigo	--light-blue	--light-green
	--lime	--orange	--pink		--purple
	--red	--teal		--yellow
	_EOF_
fi
