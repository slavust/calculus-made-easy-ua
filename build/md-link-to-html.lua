function Link (link)
  link.target = link.target:gsub('(.+)%.md%#(.+)', '%1.html#%2')
  return link
end