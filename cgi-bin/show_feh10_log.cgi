#!/usr/bin/perl

use CGI;

# character code : UTF-8

################################################################################
# Show Log
# Copyright(C) 2026 Yoshitaka Oyamatsu All rights reserved.
#
# Created : 2026/06/20(Sa)
# Updated : 
# Author  : Yoshitaka Oyamatsu
# Version : 0.0
################################################################################

require '/home/ms001641/lib/perl/sha1_utils.pl';

# パスワードファイルのパス（公開ディレクトリの外に置く）
my $password_file = "/home/ms001641/.show_log_password";

# ログファイルのパス
my $log_file = "/home/ms001641/public_html/log/feh10_access_log.txt";

my $q = CGI->new;

print $q->header(-type => 'text/html', -charset => 'UTF-8');

# パスワードファイルからハッシュを読み込む
open(my $pfh, '<', $password_file) or die "Cannot open password file: $!";
my $stored_hash = <$pfh>;
chomp $stored_hash;
close($pfh);

my $password      = $q->param('password') || '';
my $authenticated = ($password ne '' && sha1_hash($password) eq $stored_hash);

#-------------------------------------------------------------------------------
# HTMLエスケープ
#-------------------------------------------------------------------------------
sub html_escape {
    my ($str) = @_;

    $str =~ s/&/&amp;/g;
    $str =~ s/</&lt;/g;
    $str =~ s/>/&gt;/g;
    $str =~ s/"/&quot;/g;

    return $str;
}

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
    <title>Access Log</title>
    <link rel="stylesheet" type="text/css" href="/lib/StyleSheet/showLogStyle.css">
</head>
<body>
    <div id="page-header">
        <h2>Access Log</h2>
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
            ? html_escape($hostname) . '<br><span class="ip">' . html_escape($ip) . '</span>'
            : html_escape($ip);

        my $referer_cell = ($referer eq '-' || $referer eq '')
            ? '<span class="none">-</span>'
            : '<a href="' . html_escape($referer) . '" target="_blank" rel="noopener">' . html_escape($referer) . '</a>';

        print "            <tr>\n";

        if ($ip eq '133.202.106.174' || $ip eq '49.97.14.169') {
            print "                <td class='datetime myip'>"  . html_escape($datetime) . "</td>\n";
            print "                <td class='ip-address myip'>$host_cell</td>\n";
            print "                <td class='myip'>"           . html_escape($method)   . "</td>\n";
            print "                <td class='host-path myip'>" . html_escape($path)     . "</td>\n";
            print "                <td class='referrer myip'>$referer_cell</td>\n";
            print "                <td class='myip'>"           . html_escape($ua)       . "</td>\n";
        } elsif ($ip eq '45.156.128.64'        ||
                 $ip eq '109.105.209.7'        ||
                 $ip eq '157.173.122.176'      ||
                 $ip eq '199.45.154.146'       ||
                 $ip eq '134.209.84.79'        ||
                 $ip eq '18.246.159.3'         ||
                 $hostname =~ /dataprovider/   ||
                 $hostname =~ /ahrefs/         ||
                 $ua       =~ /Go-http-client/ ||
                 $ua       =~ /Cortex-Xpanse/  ||
                 $ua       =~ /SaaSBrowserBot/ ||
                 $ua       =~ /CMS-Checker/    ||
                 $ua       =~ /2ip bot/        ||
                 $ua       =~ /Who\.is Bot/    ||
                 $ua       =~ /GPTBot/         ||
                 $ua       =~ /rootevidence\.com$/) {
            print "                <td class='datetime dangerous-ip'>"  . html_escape($datetime) . "</td>\n";
            print "                <td class='ip-address dangerous-ip'>$host_cell</td>\n";
            print "                <td class='dangerous-ip'>"           . html_escape($method)   . "</td>\n";
            print "                <td class='host-path dangerous-ip'>" . html_escape($path)     . "</td>\n";
            print "                <td class='referrer dangerous-ip'>$referer_cell</td>\n";
            print "                <td class='dangerous-ip'>"           . html_escape($ua)       . "</td>\n";
        } else {
            print "                <td class='datetime'>"  . html_escape($datetime) . "</td>\n";
            print "                <td class='ip-address'>$host_cell</td>\n";
            print "                <td>"                   . html_escape($method)   . "</td>\n";
            print "                <td class='host-path'>" . html_escape($path)     . "</td>\n";
            print "                <td class='referrer'>$referer_cell</td>\n";
            print "                <td>"                   . html_escape($ua)       . "</td>\n";
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
