#!/usr/bin/perl

# パスワードファイルのパス
my $password_file = "/home/ms001641/.show_log_password";

use CGI;
use MIME::Base64;
my $q = CGI->new;

print $q->header(-type => 'text/html', -charset => 'UTF-8');

# SHA1をPure Perlで実装
sub sha1 {
    my ($msg) = @_;
    my ($h0,$h1,$h2,$h3,$h4) = (0x67452301,0xEFCDAB89,0x98BADCFE,0x10325476,0xC3D2E1F0);
    my $bits = length($msg) * 8;
    $msg .= "\x80";
    $msg .= "\x00" x ((55 - length($msg) % 64 + 64) % 64 + (length($msg) % 64 > 55 ? 64 : 0));
    $msg .= pack("N2", $bits >> 32, $bits & 0xFFFFFFFF);
    for (my $i = 0; $i < length($msg); $i += 64) {
        my @w = unpack("N16", substr($msg, $i, 64));
        for my $j (16..79) {
            my $v = $w[$j-3] ^ $w[$j-8] ^ $w[$j-14] ^ $w[$j-16];
            $w[$j] = (($v << 1) | ($v >> 31)) & 0xFFFFFFFF;
        }
        my ($a,$b,$c,$d,$e) = ($h0,$h1,$h2,$h3,$h4);
        for my $j (0..79) {
            my ($f,$k);
            if    ($j < 20) { $f = ($b & $c) | ((~$b) & $d); $k = 0x5A827999; }
            elsif ($j < 40) { $f = $b ^ $c ^ $d;              $k = 0x6ED9EBA1; }
            elsif ($j < 60) { $f = ($b & $c) | ($b & $d) | ($c & $d); $k = 0x8F1BBCDC; }
            else            { $f = $b ^ $c ^ $d;              $k = 0xCA62C1D6; }
            my $tmp = ((($a << 5) | ($a >> 27)) & 0xFFFFFFFF) + $f + $e + $k + $w[$j];
            $tmp &= 0xFFFFFFFF;
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

sub sha1_hash {
    return encode_base64(sha1($_[0]), "");
}

# パスワードファイルから現在のハッシュを読み込む
open(my $pfh, '<', $password_file) or die "Cannot open password file: $!";
my $stored_hash = <$pfh>;
chomp $stored_hash;
close($pfh);

my $current  = $q->param('current')  || '';
my $new_pass = $q->param('new_pass') || '';
my $confirm  = $q->param('confirm')  || '';
my $message  = '';
my $success  = 0;

if ($current ne '') {
    if (sha1_hash($current) ne $stored_hash) {
        $message = '<p style="color:red">現在のパスワードが違います</p>';
    } elsif ($new_pass eq '') {
        $message = '<p style="color:red">新しいパスワードを入力してください</p>';
    } elsif ($new_pass ne $confirm) {
        $message = '<p style="color:red">新しいパスワードが一致しません</p>';
    } elsif (length($new_pass) < 8) {
        $message = '<p style="color:red">パスワードは8文字以上にしてください</p>';
    } else {
        # 新しいパスワードをハッシュ化して保存
        my $new_hash = sha1_hash($new_pass);
        open(my $wfh, '>', $password_file) or die "Cannot write password file: $!";
        print $wfh $new_hash;
        close($wfh);
        $message = '<p style="color:#4c4">パスワードを変更しました</p>';
        $success  = 1;
    }
}

print <<HTML;
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>パスワード変更</title>
<style>
body { font-family: sans-serif; background: #1a1a1a; color: #ccc;
       display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
div { background: #2a2a2a; padding: 40px; border-radius: 8px; min-width: 300px; }
input { padding: 8px; margin: 4px 0; width: 100%; box-sizing: border-box; }
button { padding: 8px 20px; background: #444; color: #fff; border: none; cursor: pointer; margin-top: 10px; }
a { color: #aaa; font-size: 12px; display: block; margin-top: 15px; }
</style>
</head>
<body>
<div>
<h2>パスワード変更</h2>
$message
HTML

if ($success) {
    print '<a href="/cgi-bin/show_log.cgi">← ログイン画面へ戻る</a>';
} else {
    print <<HTML;
<form method="post" action="/cgi-bin/change_password.cgi">
<p>現在のパスワード：<br><input type="password" name="current"></p>
<p>新しいパスワード：<br><input type="password" name="new_pass"></p>
<p>新しいパスワード（確認）：<br><input type="password" name="confirm"></p>
<button type="submit">変更する</button>
</form>
<a href="/cgi-bin/show_log.cgi">← ログイン画面へ戻る</a>
HTML
}

print '</div></body></html>';
