#!/usr/bin/perl
use strict;
use DBI;
use Getopt::Std;
use utf8;

my $dbh;
my $sth;
my $rv;
my $isxn_pt_a;
my $isxn_pt_y;
my $isxn_pt_z;
my @isxn_array;
my $line;
my $bib_num;
my $oclc_num;
my @author_array;
my $author_q;
my $string;
my $start;
my $end;
my $var_let;
my $oclc_q;
my $val;
my $last_line_blank = 0;
my $fulltext;
my $ft_q;
my $branches;
my @branches;
my @branch_array;
my $branch_q;
my $mat_type;
my $mat_type_q;
my $order_num;
my @order_array;
my $order_num_q;
my $checkin_num;
my @checkin_array;
my $checkin_num_q;
my $item_num;
my @item_array;
my $item_num_q;
my @entries;
my $entry;


my $delim_baseDir = "/home/bfreels";
# my $delim_baseDir = "c:\\aa\\libros";
my $infile = "cswrholdingstext.txt";

opendir(SGMLDIR, "$delim_baseDir\/text") or die "Can’t open $delim_baseDir\/text:  $!";

@entries = readdir(SGMLDIR);

closedir(SGMLDIR);

foreach $entry (@entries) {
  if ($entry ne '.' && $entry ne '..') {
    open (SGMLFILE, "$delim_baseDir\/$entry") or die "Can't open $delim_baseDir\/$entry.";
    process_file();
    close SGMLFILE;
  }
}

sub process_file {
    while ($line = <SGMLFILE>) {
        # CLEAR VARIABLES AT LEADER
        if ($line =~ /^[\r\n]+$/) {
            if ($last_line_blank && $last_line_blank == 1) {
                to_db();
                # UNSET VARS
                $last_line_blank = 0;
                undef @item_array;
                undef @order_array;
                undef @checkin_array;
                next;
            } else {
                $last_line_blank = 1;
                next;
            }
        } else {
            $last_line_blank = 0;
            if ($line =~ /(^ B[^\s]+)/) {
                $fulltext = "";
                $bib_num = "$1";
                $bib_num =~ s/[\sB]+//g;
                $fulltext .= " " . $line;
            } elsif ($line =~ /LOCATIONS\s+(.+)\s+/) {
                $branches = $1;
                $fulltext .= " " . $line;
            } elsif ($line =~ /MAT TYPE:\s+([a-z]+)[\s.]+/) {
                $mat_type = $1;
                $fulltext .= " " . $line;
            } elsif ($line =~ /(^ I[^\s]+)/) {
                $item_num = "$1";
                $item_num =~ s/[\sI]+//g;
                push(@item_array, $item_num);
                $fulltext .= " " . $line;
            } elsif ($line =~ /(^ O[^\s]+)/) {
                $order_num = "$1";
                $order_num =~ s/[\sO]+//g;
                push(@order_array, $order_num);
                $fulltext .= " " . $line;
            } elsif ($line =~ /(^ C[^\s]+)/) {
                $checkin_num = "$1";
                $checkin_num =~ s/[\sC]+//g;
                push(@checkin_array, $checkin_num);
                $fulltext .= " " . $line;
            } else {
                $fulltext .= " " . $line;
            }
            next;
        }
    }
}


# Sub declarations

sub to_db {
            print "Bibno.: $bib_num\n";
    if (($bib_num && $bib_num ne '') && ($fulltext && $fulltext ne '')) {
        $dbh = DBI->connect("DBI:mysql:database=libros;host=localhost","libros_user","librospass");
        if (!$dbh) { print 'could not connect to database';
            exit;
        } else {
            print "DB connections established.\n\n";
        }
        $ft_q = "insert into full_record (full_record_full_record, full_record_id) values (?, ?)";
        $sth = $dbh->prepare($ft_q) or die "Can't prepare $ft_q: $dbh->errstr\n";
        $rv = $sth->execute($fulltext, $bib_num) or die "can't execute the query: $sth->errstr\n";
        if ($branches && $branches ne '') {
            @branch_array = split(',', $branches);
            foreach (@branch_array) {
                $branch_q = "insert into branch (branch_branch, branch_full_record_id) values (?, ?)";
                $sth = $dbh->prepare($branch_q) or die "Can't prepare $branch_q: $dbh->errstr\n";
                $rv = $sth->execute($_, $bib_num) or die "can't execute the query: $sth->errstr\n";
            }
        }
        if ($mat_type && $mat_type ne '') {
            $mat_type_q = "insert into material_type (material_type_material_type, material_type_full_record_id) values (?, ?)";
            $sth = $dbh->prepare($mat_type_q) or die "Can't prepare $mat_type_q: $dbh->errstr\n";
            $rv = $sth->execute($mat_type, $bib_num) or die "can't execute the query: $sth->errstr\n";
        }
        if (@item_array && @item_array ne '') {
            foreach (@item_array) {
                $item_num_q = "insert into item_number (item_number_item_number, item_number_full_record_id) values (?, ?)";
                $sth = $dbh->prepare($item_num_q) or die "Can't prepare $item_num_q: $dbh->errstr\n";
                $rv = $sth->execute($_, $bib_num) or die "can't execute the query: $sth->errstr\n";
            }
        }
        if (@order_array && @order_array ne '') {
            foreach (@order_array) {
                $order_num_q = "insert into order_number (order_number_order_number, order_number_full_record_id) values (?, ?)";
                $sth = $dbh->prepare($order_num_q) or die "Can't prepare $order_num_q: $dbh->errstr\n";
                $rv = $sth->execute($_, $bib_num) or die "can't execute the query: $sth->errstr\n";
            }
        }
        if (@checkin_array && @checkin_array ne '') {
            foreach (@checkin_array) {
                $checkin_num_q = "insert into checkin_number (checkin_number_checkin_number, checkin_number_full_record_id) values (?, ?)";
                $sth = $dbh->prepare($checkin_num_q) or die "Can't prepare $checkin_num_q: $dbh->errstr\n";
                $rv = $sth->execute($_, $bib_num) or die "can't execute the query: $sth->errstr\n";
            }
        }
        $dbh->disconnect;
 
    }
}








# Insert query:
# insert into article(collection_id,year,author,title,volume,abstract,subject,pdf_url,djvu_url,html_url,body,volume_number,issue_number,issue_period)
# values($CID,$qdat,$qaut,$qtit,$qvol,$qabs,$qsub,$qpdf,$qdjv,$qhtm,$qtxt,$qvoln,$qissn,$qissp)



