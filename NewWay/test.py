
from context import Context






s = Context()

# how to have input layer?...Need input layer? lolz

ps = PretendStimulus(....)

s.add_node('photoreceptor', is_worker=True, ..., focus=True)




# how to assign inputs appropriately? 
# just...add a function to each node that allows it to get the next relevant
# stimulus point...could pass own position to stimulus, then stimulus returns 
# relevant value?'
# and do positioning as before, with just a function that each unit can ask
# for a position from.
# should have a way to reset distribution functions when simulation is reset?

# something like
s.add_step('update', store(access_input, ps)) # have s.store? will passing ps like this work?
# or something
# and access_input basically gets a node to pass its position to ps and then update its output in the right way
# alternately, why not just subclass Node to make something custom-made for accessing input?
# can make a few subclasses and then get rid of some of the options in init for node
