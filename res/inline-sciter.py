#!/usr/bin/env python3

import re


def strip(s): return re.sub(r'\s+\n', '\n', re.sub(r'\n\s+', '\n', s))

def read_file(path):
    with open(path, encoding='utf-8') as f:
        return f.read()

common_css = read_file('src/ui/common.css')
common_tis = read_file('src/ui/common.tis')

index = read_file('src/ui/index.html') \
    .replace('@import url(index.css);', read_file('src/ui/index.css')) \
    .replace('include "index.tis";', read_file('src/ui/index.tis')) \
    .replace('include "msgbox.tis";', read_file('src/ui/msgbox.tis')) \
    .replace('include "ab.tis";', read_file('src/ui/ab.tis'))

remote = read_file('src/ui/remote.html') \
    .replace('@import url(remote.css);', read_file('src/ui/remote.css')) \
    .replace('@import url(header.css);', read_file('src/ui/header.css')) \
    .replace('@import url(file_transfer.css);', read_file('src/ui/file_transfer.css')) \
    .replace('include "remote.tis";', read_file('src/ui/remote.tis')) \
    .replace('include "msgbox.tis";', read_file('src/ui/msgbox.tis')) \
    .replace('include "grid.tis";', read_file('src/ui/grid.tis')) \
    .replace('include "header.tis";', read_file('src/ui/header.tis')) \
    .replace('include "file_transfer.tis";', read_file('src/ui/file_transfer.tis')) \
    .replace('include "port_forward.tis";', read_file('src/ui/port_forward.tis')) \
    .replace('include "printer.tis";', read_file('src/ui/printer.tis'))

chatbox = read_file('src/ui/chatbox.html')
install = read_file('src/ui/install.html').replace('include "install.tis";', read_file('src/ui/install.tis'))

cm = read_file('src/ui/cm.html') \
    .replace('@import url(cm.css);', read_file('src/ui/cm.css')) \
    .replace('include "cm.tis";', read_file('src/ui/cm.tis'))


def compress(s):
    s = s.replace("\r\n", "\n")
    x = bytes(s, encoding='utf-8')
    return '&[u8; ' + str(len(x)) + '] = b"' + str(x)[2:-1].replace(r"\'", "'").replace(r'"',
                                                                                  r'\"') + '"'


with open('src/ui/inline.rs', 'wt') as fh:
    fh.write('const _COMMON_CSS: ' + compress(strip(common_css)) + ';\n')
    fh.write('const _COMMON_TIS: ' + compress(strip(common_tis)) + ';\n')
    fh.write('const _INDEX: ' + compress(strip(index)) + ';\n')
    fh.write('const _REMOTE: ' + compress(strip(remote)) + ';\n')
    fh.write('const _CHATBOX: ' + compress(strip(chatbox)) + ';\n')
    fh.write('const _INSTALL: ' + compress(strip(install)) + ';\n')
    fh.write('const _CONNECTION_MANAGER: ' + compress(strip(cm)) + ';\n')
    fh.write('''
fn get(data: &[u8]) -> String {
    String::from_utf8_lossy(data).to_string()
}
fn replace(data: &[u8]) -> String {
    let css = get(&_COMMON_CSS[..]);
    let res = get(data).replace("@import url(common.css);", &css);
    let tis = get(&_COMMON_TIS[..]);
    res.replace("include \\\"common.tis\\\";", &tis)
}
#[inline]
pub fn get_index() -> String {
    replace(&_INDEX[..])
}
#[inline]
pub fn get_remote() -> String {
    replace(&_REMOTE[..])
}
#[inline]
pub fn get_install() -> String {
    replace(&_INSTALL[..])
}
#[inline]
pub fn get_chatbox() -> String {
    replace(&_CHATBOX[..])
}
#[inline]
pub fn get_cm() -> String {
    replace(&_CONNECTION_MANAGER[..])
}
''')
