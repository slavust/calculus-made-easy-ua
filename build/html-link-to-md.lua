function Link (link)
  link.target = link.target:gsub('(.+)%.html%#(.+)', '%1.md#%2')
  return link
end