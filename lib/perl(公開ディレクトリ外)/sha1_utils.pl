################################################################################
# SHA1 Utility
# Copyright(C) 2026 Yoshitaka Oyamatsu All rights reserved.
#
# Created : 2026/06/07(Su)
# Updated :
# Author  : Yoshitaka Oyamatsu
# Version : 0.0
################################################################################

use MIME::Base64;

#-------------------------------------------------------------------------------
# SHA1ハッシュ値生成
#-------------------------------------------------------------------------------
sub sha1 {
    my ($msg)                = @_;
    my ($h0,$h1,$h2,$h3,$h4) = (0x67452301,0xEFCDAB89,0x98BADCFE,0x10325476,0xC3D2E1F0);
    my $bits_lo              = length($msg) * 8;

    $msg .= "\x80";
    while (length($msg) % 64 != 56) {
        $msg .= "\x00";
    }

    $msg .= pack("NN", 0, $bits_lo);
    for (my $i = 0; $i < length($msg); $i += 64) {
        my @w = unpack("N16", substr($msg, $i, 64));
        for my $j (16..79) {
            my $v  = $w[$j-3] ^ $w[$j-8] ^ $w[$j-14] ^ $w[$j-16];
            $w[$j] = (($v << 1) | ($v >> 31)) & 0xFFFFFFFF;
        }

        my ($a,$b,$c,$d,$e) = ($h0,$h1,$h2,$h3,$h4);
        for my $j (0..79) {
            my ($f,$k);

            if ($j < 20) {
                $f = ($b & $c) | ((0xFFFFFFFF ^ $b) & $d);
                $k = 0x5A827999;
            } elsif ($j < 40) {
                $f = $b ^ $c ^ $d;
                $k = 0x6ED9EBA1;
            } elsif ($j < 60) {
                $f = ($b & $c) | ($b & $d) | ($c & $d);
                $k = 0x8F1BBCDC;
            } else {
                $f = $b ^ $c ^ $d;
                $k = 0xCA62C1D6;
            }

            my $tmp = ((($a << 5) | ($a >> 27)) + $f + $e + $k + $w[$j]) & 0xFFFFFFFF;
            ($a,$b,$c,$d,$e) = ($tmp, $a, (($b<<30)|($b>>2))&0xFFFFFFFF, $c, $d);
        }

        $h0 = ($h0 + $a) & 0xFFFFFFFF;
        $h1 = ($h1 + $b) & 0xFFFFFFFF;
        $h2 = ($h2 + $c) & 0xFFFFFFFF;
        $h3 = ($h3 + $d) & 0xFFFFFFFF;
        $h4 = ($h4 + $e) & 0xFFFFFFFF;
    }

    return pack("N5", $h0,$h1,$h2,$h3,$h4);
}

#-------------------------------------------------------------------------------
# 生成したSHA1ハッシュ値をBASE64へ符号化
#-------------------------------------------------------------------------------
sub sha1_hash {
    return encode_base64(sha1($_[0]), "");
}

1;
