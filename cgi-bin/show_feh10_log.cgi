#!/usr/bin/perl

use CGI;

# character code : UTF-8

################################################################################
# Show Log
# Copyright(C) 2026 Yoshitaka Oyamatsu All rights reserved.
#
# Created : 2026/06/20(Sa)
# Updated : 2026/06/21(Su)
# Author  : Yoshitaka Oyamatsu
# Version : 0.1
################################################################################

my $q = CGI->new;

eval {
    require '/home/ms001641/lib/perl/sha1_utils.pl';
    require '/home/ms001641/public_html/cgi-bin/common_functions.pl';

    1;
} or do {
    my $err = $@ || 'Unknown error';

    print $q->header(-type => 'text/html', -charset => 'UTF-8');
    print <<HTML;
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="robots" content="noindex, nofollow">
    <title>Access Log - Error</title>
</head>
<body>
    <p>内部エラーが発生しました。しばらくしてから再度お試しください。</p>
</body>
</html>
HTML

    exit;
};

# パスワードファイルのパス（公開ディレクトリの外に置く）
my $password_file = "/home/ms001641/.show_log_password";

# ログファイルのパス
my $log_file = "/home/ms001641/public_html/log/feh10_access_log.txt";

print $q->header(-type => 'text/html', -charset => 'UTF-8');

# パスワードファイルからハッシュを読み込む
open(my $pfh, '<', $password_file) or die "Cannot open password file: $!";
my $stored_hash = <$pfh>;
chomp $stored_hash;
close($pfh);

my $password      = $q->param('password') || '';
my $authenticated = ($password ne '' && sha1_hash($password) eq $stored_hash);

#-------------------------------------------------------------------------------
# メイン処理
#-------------------------------------------------------------------------------
if ($authenticated) {
    open(my $fh, '<', $log_file) or die "Cannot open: $!";
    my @lines = <$fh>;
    close($fh);

    print <<HTML;
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="robots" content="noindex, nofollow">
    <title>Feh10 Access Log</title>
    <link rel="stylesheet" type="text/css" href="/lib/StyleSheet/showLogStyle.css">
</head>
<body>
    <div id="page-header">
        <h2>Feh10 Access Log</h2>
        <a href="/cgi-bin/change_password.cgi">パスワード変更</a>
    </div>
    <table>
        <thead>
            <tr>
                <th>日時</th>
                <th>IPアドレス</th>
                <th>メソッド</th>
                <th>ホスト／パス</th>
                <th>リファラ</th>
                <th>User-Agent</th>
            </tr>
        </thead>
        <tbody>
HTML

    foreach my $line (reverse @lines) {
        chomp $line;
        next if $line eq '';

        my ($datetime, $host, $method, $path, $referer, $ua) = split(/\t/, $line, 6);

        # ホスト名(IPアドレス) の形式を分離して表示
        my ($hostname, $ip);
        if ($host =~ /^(.+)\(([^)]+)\)$/) {
            $hostname = $1;
            $ip       = $2;
        } else {
            $hostname = '';
            $ip       = $host;
        }

        my $host_cell = $hostname
            ? commonFunctionsPackage::html_escape($hostname) . '<br><span class="ip">' . commonFunctionsPackage::html_escape($ip) . '</span>'
            : commonFunctionsPackage::html_escape($ip);

        my $referer_cell = ($referer eq '-' || $referer eq '')
            ? '<span class="none">-</span>'
            : '<a href="' . commonFunctionsPackage::html_escape($referer) . '" target="_blank" rel="noopener">' . commonFunctionsPackage::html_escape($referer) . '</a>';

        print "            <tr>\n";

        if (commonFunctionsPackage::my_ip_check($ip)) {
            print "                <td class='datetime myip'>"  . commonFunctionsPackage::html_escape($datetime) . "</td>\n";
            print "                <td class='ip-address myip'>$host_cell</td>\n";
            print "                <td class='myip'>"           . commonFunctionsPackage::html_escape($method)   . "</td>\n";
            print "                <td class='host-path myip'>" . commonFunctionsPackage::html_escape($path)     . "</td>\n";
            print "                <td class='referrer myip'>$referer_cell</td>\n";
            print "                <td class='myip'>"           . commonFunctionsPackage::html_escape($ua)       . "</td>\n";
        } elsif (commonFunctionsPackage::alert_ip_check($ip)             ||
                 commonFunctionsPackage::alert_hostname_check($hostname) ||
                 commonFunctionsPackage::alert_ua_chech($ua)) {
            print "                <td class='datetime dangerous-ip'>"  . commonFunctionsPackage::html_escape($datetime) . "</td>\n";
            print "                <td class='ip-address dangerous-ip'>$host_cell</td>\n";
            print "                <td class='dangerous-ip'>"           . commonFunctionsPackage::html_escape($method)   . "</td>\n";
            print "                <td class='host-path dangerous-ip'>" . commonFunctionsPackage::html_escape($path)     . "</td>\n";
            print "                <td class='referrer dangerous-ip'>$referer_cell</td>\n";
            print "                <td class='dangerous-ip'>"           . commonFunctionsPackage::html_escape($ua)       . "</td>\n";
        } else {
            print "                <td class='datetime'>"  . commonFunctionsPackage::html_escape($datetime) . "</td>\n";
            print "                <td class='ip-address'>$host_cell</td>\n";
            print "                <td>"                   . commonFunctionsPackage::html_escape($method)   . "</td>\n";
            print "                <td class='host-path'>" . commonFunctionsPackage::html_escape($path)     . "</td>\n";
            print "                <td class='referrer'>$referer_cell</td>\n";
            print "                <td>"                   . commonFunctionsPackage::html_escape($ua)       . "</td>\n";
        }

        print "            </tr>\n";
    }

    print <<HTML;
        </tbody>
    </table>
</body>
</html>
HTML

} else {
    my $error = ($password ne '')
                ? '<p style="color:red">パスワードが違います</p>' : '';
    print <<HTML;
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="robots" content="noindex, nofollow">
    <title>Feh10 Access Log - Login</title>
    <link rel="stylesheet" type="text/css" href="/lib/StyleSheet/showLogLoginStyle.css">
</head>
<body>
    <div>
        <h2>Access Log</h2>
        $error
        <form method="post" action="/cgi-bin/show_feh10_log.cgi">
            <p>パスワード：<input type="password" name="password"></p>
            <p><button type="submit">ログイン</button></p>
        </form>
    </div>
</body>
</html>
HTML
}
