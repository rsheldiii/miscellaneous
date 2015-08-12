class BF
  def initialize(prgm)
    @dptr, @iptr = 0, 0
    @darr = Hash.new(0)
    @br = []
    @prgm = prgm
    step { |c| exec(c) } while @iptr < @prgm.length
  end
 
  def step
    @iptr += 1 if yield(@prgm[@iptr].ord)
  end

  def exec(chr)
    {
      62 => ->{ @dptr += 1 },
      60 => ->{ @dptr -= 1 },
      43 => ->{ @darr[@dptr] += 1 },
      45 => ->{ @darr[@dptr] -= 1 },
      46 => ->{ print @darr[@dptr].chr },
      44 => ->{ @darr[@dptr] = gets[0].to_i },
      91 => ->{ @darr[@dptr] == 0 ? jmp : @br << @iptr },
      93 => ->{ @iptr = @br.pop - 1 }
    }[chr].call || true
  end

  def jmp
    f = (@iptr += 1) > 0
    step { |chr| f = chr == 93 ? false : chr == 91 ? jmp || true : true } while f
  end
end

BF.new("++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.")
