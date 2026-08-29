#!/usr/bin/perl

# パスワード設定
my $correct_password = "2k26May30Fx4Wd";

# ログファイルのパス
my $log_file = "/home/ms001641/public_html/log/mylog.txt";

use CGI;
my $q = CGI->new;

print $q->header(-type => 'text/html', -charset => 'UTF-8');

my $password = $q->param('password') || '';

# パスワードが正しい場合はログを表示
if ($password eq $correct_password) {
    open(my $fh, '<', $log_file) or die "Cannot open: $!";
    my @lines = <$fh>;
    close($fh);

    print <<HTML;
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>Access Log</title>
<style>
body { font-family: monospace; font-size: 12px; background: #1a1a1a; color: #ccc; padding: 20px; }
pre { white-space: pre-wrap; word-break: break-all; }
</style>
</head>
<body>
<h2>Access Log</h2>
<pre>
HTML
    foreach my $line (reverse @lines) {
        $line =~ s/&/&amp;/g;
        $line =~ s/</&lt;/g;
        $line =~ s/>/&gt;/g;
        print $line;
    }
    print "</pre></body></html>";

} else {
    # パスワード入力フォームを表示
    my $error = ($password ne '' && $password ne $correct_password) 
                ? '<p style="color:red">パスワードが違います</p>' : '';
    print <<HTML;
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>Access Log - Login</title>
<style>
body { font-family: sans-serif; background: #1a1a1a; color: #ccc; 
       display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
div { background: #2a2a2a; padding: 40px; border-radius: 8px; }
input { padding: 8px; margin: 8px 0; width: 200px; }
button { padding: 8px 20px; background: #444; color: #fff; border: none; cursor: pointer; }
</style>
</head>
<body>
<div>
<h2>Access Log</h2>
$error
<form method="post" action="/cgi-bin/show_log.cgi">
<p>パスワード：<input type="password" name="password"></p>
<p><button type="submit">ログイン</button></p>
</form>
</div>
</body>
</html>
HTML
}
