class BF
  def initialize
    @data_ptr = 0
    @instruction_ptr = 0
    @data_array = Hash.new(0) # hash cuz nils
    @program = ""
    @brackets = [] # bracket rememberer for jumping
  end

  def run(program)
      @program = program
      process_command { |c| execute(c) } while @instruction_ptr < @program.length
  end

  #accepts a block and yields the next command. block must return true/false indicating if the instruction pointer needs to increment
  def process_command
    @instruction_ptr += 1 if yield(@program[@instruction_ptr])
  end

  def execute(chr)
    case chr
    when '>' then @data_ptr += 1
    when '<' then @data_ptr -= 1
    when '+' then @data_array[@data_ptr] += 1
    when '-' then @data_array[@data_ptr] -= 1
    when '.' then p @data_array[@data_ptr].chr
    when ',' then @data_array[@data_ptr] = gets.first.to_i #todo not correct, can get more than a byte
    when '['
      jump if @data_array[@data_ptr] == 0
      @brackets << @instruction_ptr unless @data_array[@data_ptr] == 0
    when ']' then @instruction_ptr = @brackets.pop - 1 # -1 cuz we immediately increment the instruction pointer when we successfully execute a command
    end

    return true # always increment
  end

  #call on a bracket when data ptr is 0 to jump to the matching bracket
  def jump
    counter = 0
    process_command { |c| true } # throw out the starting bracket

    while counter >=0
      process_command do |chr|
        case chr
        when '[' then counter += 1
        when ']' then counter -= 1
        end

        counter >= 0 # since this is a process_command loop inside of a process_command loop, we need to escape one instruction pointer increment
      end
    end
  end
end

a = BF.new()
a.run "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
