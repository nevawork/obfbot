"""Example obfuscated script and test utilities."""

EXAMPLE_LUA_CODE = r'''
-- Example Lua script
local function fibonacci(n)
    if n <= 1 then
        return n
    end
    return fibonacci(n - 1) + fibonacci(n - 2)
end

local function main()
    local numbers = {1, 2, 3, 4, 5}
    
    for i, num in ipairs(numbers) do
        print("Number: " .. num)
        print("Fibonacci: " .. fibonacci(num))
    end
    
    local config = {
        name = "Example",
        version = "1.0.0",
        enabled = true
    }
    
    return config
end

return main()
'''

def get_example_code() -> str:
    """Get example Lua code.
    
    Returns:
        Example Lua code
    """
    return EXAMPLE_LUA_CODE
