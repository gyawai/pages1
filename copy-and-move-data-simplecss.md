---
layout: default-simplecss-md
title: Transfer Data
---

# Transfer Data

You can transfer data between your computer and our storage systems in
several ways. You can mount Bucket as a shared folder; you can use ssh
to copy data from the terminal; use Datashare to transfer data to other
users on deigo; and you can use Rsync for fast, reliable transfer lf
large data sets.

[Access Bucket as a shared remote folder from your
desktop](#remote-folder)\
[Use ssh and sftp to copy data on the command line](#scp)\
[Quickly transfer data to other users with Datashare](#datashare)

[Fast, reliable transfer using Rsync](#advanced-copy)\
[Mount a remote directory using sshfs](#sshfs)

## Using remote folders {#remote-folder}

You can access and move data from your desktop by using `bucket` as a
remote shared folder on your desktop. The details differ by operating
system, but you mount it as a shared drive using the Samba protocol.

  |File system   |Server             |domain   |share name
  |------------- |------------------ |-------- |------------
  |`bucket`      |`bucket.oist.jp`   |OIST     |`bucket`

\
Please check the IT help pages for more information on how to mount
remote shared folders on your operating system (links go to the external
IT site):

[Windows](https://oist.service-now.com/sp?id=kb_article&sys_kb_id=0a15d14e933e31504faa7cddfaba1095)\
[Mac
OS](https://oist.service-now.com/sp?id=kb_article_view&sys_kb_id=a82796011be5ec10430898e9bc4bcb03)\
[Linux](https://oist.service-now.com/sp?id=kb_article_view&sys_kb_id=666552cd1ba5ec10430898e9bc4bcbbe)\


## Copy Files Using scp {#scp}

The \"`scp`\" command, for \"Secure CoPy\", is the main way to copy
files to and from Deigo. If you want to copy a file `myfile.txt` to
Deigo, you would open a terminal (or a MobaXTerm window) on your own
computer and do:







    $ scp myfile.txt username@deigo.oist.jp:







This command works like the regular `cp` command. The big difference is
that we can tell it to copy to remote machines. The colon at end of the
address tells `scp` that it\'s a remote machine, not a file name. If you
forget the colon you will copy `myfile.txt` to a new file with name
\"`username@deigo.oist.jp`\" which is not quite what you wanted.

If you set up aliases like described in \"[Connect to the
Clusters](https://groups.oist.jp/scs/connect-clusters#advanced-setup)\"
you can use the alias here too:







    $ scp myfile.txt deigo:







The default remote target directory is your home. You can add a path
after the colon (and note that tab completion works remotely under
Linux):







    $ scp myfile.txt deigo:/bucket/MyUnit/







Everything before the colon in `deigo:` specifies the remote computer.
Everything after the colon is the directory or file on the remote
machine. You can use shell wildcards to specify multiple files, and you
can copy from the remote machine to your local machine as well:







    $ scp deigo:some_directory/* .







This would copy all the files in directory `some_directory` in your home
on Deigo to the current directory on your local computer. If you add the
`-r` option, you can copy *recursively,* that is, copy all files in all
subdirectories. The below command will copy `somedir` and all its data:







    $ scp -r deigo:somedir .







###  Browse interactively using `sftp`

`sftp` (do not confuse it with `ftps`, another protocol) is a simple
protocol to browse and copy files interactively over ssh. You can use it
on the command line:







    $ sftp <your oist-id>@deigo.oist.jp







The most common commands are:

  |command        |description
  |-------------- |-------------------------------------
  |cd             |change directory on the remote side
  |lcd            |change direcory locally
  |ls             |list contents of remote directory
  |put \[file\]   |upload \[file\] to remote
  |get \[file\]   |download \[file\] from remote

Use the \"`help`\" command to see a list of commands.

The command line client works, but if you run Linux you can also use
sftp through your file browser.

On Linux you can use the Nautilus file browser (default on most
desktops) to connect and browse, copy and move files via sftp. Select
\"connect to server\" or just press `ctrl-l`. Then enter
`sftp://deigo.oist.jp`, enter your OIST ID and password, and you will be
able to browse and handle your remote files.

By default you can just see your home directory. To get to, say, Bucket,
you need to edit the location. Press `ctrl-l`. Your location will look
like \"`sftp://deigo.oist.jp/`\". Add \"bucket\" to the end, like
\"`sftp://deigo.oist.jp/bucket`\", to browse /bucket instead. You can
add a bookmark to reconnect easily if you like.

Windows and OSX does not support `sftp` by default, but there are a
number of sftp clients for free download that will let you access Deigo
in a file browser in much the same way.

### Datashare {#datashare}

The Deigo login nodes have a directory (storage system) called
Datashare, mounted as `/datashare`. It\'s meant for quick, temporary
sharing of data to workshop participants, or for members of different
units that need to transfer data to each other.

If you copy data to Datashare it will automatically become **readable**
to anybody. Any data there will also be **deleted** after about one day
if you forget to delete it yourself.

If you want to transfer a file to somebody else, follow these steps:

1.  From a login node, copy the data to /datashare.
2.  Ask the recipients to log in and copy the data from /datashare to
    their own bucket or home.
3.  Once they\'ve done this, delete the data.

Note: All data here is *publicly readable*. Don\'t use Datashare to
transfer restricted or confidential data!

## Advanced file access {#advanced-copy}

### Rsync

`rsync` is an advanced program for synchronizing directories and copying
large number of files locally or over a network using ssh.

Before the copy, rsync compares the source and destination. Only the
files that have changed, and (normally) only the changes to each file
are actually transferred.

-   If you use rsync to keep two directories in sync between your local
    and remote machines, only the changes since the last sync will be
    transferred. This greatly reduces the amount of time you need to
    synchronize them.

-   If rsync is interrupted - because you lost the connection, or
    because you had to leave and turn off the computer for instance - it
    will pick up again where it left off instead of starting over. This
    makes rsync a very dependable way to copy data over slow or
    unreliable network connections.

It is quite a complicated program with many options, so we refer you to
the main documentation. Here are a couple of common examples:







    $ rsync -av --no-group --no-perms mydir/ deigo:target-dir/







This sends the content of \"mydir\" into \"target-dir\". Note the \"/\"
at the end; rsync takes this to mean you want to copy the contents
inside. You end up with \"target-dir/\".

The flag \"-a\" is short for \"archive\". It will copy all file
attributes as well, such as creation and modification dates, links,
permissions, ownership and so on. \"-v\" means to be verbose and print
out what rsync is doing. \"\--no-group\" and \"\--no-perms\" makes sure
we don\'t copy ownership and permissions, as they are different on the
remote system.



    $ rsync -av --no-group --no-perms mydir deigo:target-dir/



This sends \"mydir\" itself and its contents into \"target-dir\".
Without a \"/\" at the end, rsync will copy the directory itself, so you
get \"target-dir/mydir/\"



    $ rsync -av --no-group --no-perms --partial mybigfiles/ deigo:target-dir/



For very large files (gigabytes or more), resending the entire file if
it got interrupted would waste a lot of time. The \"\--partial\" option
tells rsync not to delete partial files, but to pick up where it left
off.\




    $ rsync -av --no-group --no-perms --del --exclude=*bk deigo:datadir localdir



Synchronize everything in \"datadir\" on Deigo with \"localdir\" on the
local machine. Delete any files in \"localdir\" that are not in
\"datadir\" (that is, if they were deleted in \"datadir\" they\'ll be
deleted locally as well). Exclude any file that ends in \"bk\".

### sshfs {#sshfs}

\"`sshfs`\" is a \"pseudo-filesystem\" that you can use on Linux and
OSX. It will connect a remote and a local directory, much like mounting
a remote filesystem. In the background it uses sftp to actually transfer
the data, but it lets you treat your remote directory as a part of your
regular filesystem.

First you need to get sshfs. On Linux it is available from your
distributions package manager. On OSX you may need to install it through
one of the open source distribution systems. Once you installed it, the
format for starting it is:







    $ sshfs [options] deigo:datadir localdir/







This will mount \"datadir\" on Deigo onto \"localdir\" on your local
computer. \"localdir\" needs to be an empty directory. Ideally you would
make a specific subdirectory, one for each remote, in a \"`mount`\"
directory:







    $ mkdir -p mount/deigo







If there\'s no activity, ssh will normally close the connection after
some time. That is very inconvenient when you use it as a file system.
Also, sshfs will by default not try to reconnect if it loses connection.
Finally, your user ID is different on the local and remote machine, and
we want to make sure any files are presented with the right ownership.

You will want to use three options for sshfs: \"`reconnect`\" to make it
reconnect; \"`idmap=user`\" to resolve user identity differences; and
\"`ServerAliveInterval=30`\" to keep the connection alive and to detect
if it disconnects, by pinging the server every 30 seconds.

Let\'s say I want to mount my `/bucket/UnitU/mydata/` directory on
Deigo, and mount it locally on `mount/deigo`. I would do this as:







    $ sshfs -o reconnect,idmap=user,ServerAliveInterval=30 deigo:/bucket/UnitU/mydata mount/deigo







That command is a mouthful, so you may want to put this in a small shell
script.

You can unmount it again with \"`fusermount`\":







    $ fusermount -u mount/deigo









#### Issues

sshfs is very convenient: you can mount any directory you can reash with
ssh, in a safe, encrypted manner, and treat as a local directory without
using a VPN or any other extras. But it has a few drawbacks.

The main issue is that it does not deal well with disconnections. Any
access to the directory while it\'s disconnected will hang, waiting for
a remote reply. You can try it for yourself. Mount a directory on deigo
as above, disable wifi, then try listing the directory:







    $ ls mount/deigo







After a few seconds, the command will suddenly hang, and can\'t be
stopped. In fact, *any* software that directly or indirectly tries to
access that directory will now freeze.

Since we added the \"`ServerAliveInterval`\" option above, sshfs will
eventually give up trying and let the applications run again, but it
will still take up to a minute or so. For this reason, sshfs is really
better suited for your workstation than for a laptop that often loses
the connection as you move about.

To forcibly stop sshfs, you can force unmount the file system (you may
need to do it as root):







    $ sudo umount --force mount/deigo







You may need to repeat the command a few times before it really takes
effect.

You can also look for the actual ssh process and kill it:







    $ ps ax|grep "ssh.*sftp"
    26854 pts/23 S  0:00 ssh -x -a [...] -oServerAliveInterval=30 [...] deigo -s sftp
    $ kill -9 26854







Just be careful that you don\'t kill the wrong ssh process by mistake.

Finally, if sshfs has disconnected, the OS may still mistakenly see the
remote as mounted, so you can\'t remount. Then you can do a \"lazy\"
unmount (where it doesn\'t wait for a reponse from the server) to make
the OS release the mount point:







    $ fusermount -uz mount/deigo





