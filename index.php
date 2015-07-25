<?php
	$seed = (int)$argv[1];
	$num_adjectives = (int)$argv[2];
	$num_nouns = (int)$argv[3];
	srand($seed);

	echo rand(0,$num_adjectives - 1) , ',',rand(0,$num_nouns - 1)
?>