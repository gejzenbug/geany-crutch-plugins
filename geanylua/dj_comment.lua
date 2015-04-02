--[[
    Another little crutch for Django templates. 
    This script comment/uncomment selected lines ({# #}) and highlight its.
--]]

local sel_start, sel_end = geany.select()

if sel_start > sel_end then
    sel_start, sel_end = sel_end, sel_start
end

local line_start, col = geany.rowcol(sel_start)
local line_end, col = geany.rowcol(sel_end)

for line = line_start, line_end do
    line_string = geany.lines(line)
    open_bracket = string.find(line_string, '{#')
    close_bracket = string.find(line_string, '#}')
    p = geany.rowcol(line, 0)
    geany.select(p, p + string.len(line_string)-1)
    if open_bracket and close_bracket then
        line_string = string.sub(line_string, open_bracket+2, close_bracket-1)
    else
        line_string = string.format('{#%s#}', string.sub(line_string, 0, string.len(line_string)-1))
        geany.scintilla("SCI_SETINDICATORCURRENT", 21, 0);
        --geany.scintilla(sc.SCI_INDICSETSTYLE, 21, sc.INDIC_CONTAINER);
        --geany.scintilla(sc.SCI_INDICSETFORE, 21, 0xFF8300);
        --geany.scintilla(sc.SCI_INDICSETALPHA, DJANGO_TAG_INDICATOR, 100);
        geany.scintilla("SCI_INDICATORFILLRANGE", p-1, string.len(line_string)-2);
    end
    geany.selection(line_string)
end
