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
    geany.select(p, p + string.len(line_string))
    if open_bracket and close_bracket then
        line_string = line_string:gsub("{#", ''):gsub("#}", '')
    else
        line_string = string.format('{#%s#}\n', line_string:sub(0, line_string:len()-1))
        geany.scintilla("SCI_SETINDICATORCURRENT", 21, 0);
        geany.scintilla("SCI_INDICATORFILLRANGE", p-1, line_string:len()-2);
    end
    geany.selection(line_string)
end
