# jBrute
 Bruteforce password generator made in python

I don't know if i have to specify this because this is my first project that i make public, but... 

this is for educational purposes only, i am not responsible for anything that you do with this script
# Settings setup
(you can find some basic settings in the settings.txt file)

Settings have their own format:



To create a list containing "1","2" and "3", use

<code> test_list < 1,2,3 </code> 

To specify that when you write "?t" in the bruteforce format you are referring to the "test_list" list, use

<code> ?t = test_list </code>

You can also sum more lists and assing their sum to a single ref in this way:

<code> list1 < 1,2,3 </code>

<code> list2 < 4,5,6 </code>

<code> ?all = list1+list2 </code>

# Implementing dictionaries

You can implement a dictionary excplicitly, in the same way of list of characters

<code> test_dict < hello,world,i,am,cool </code>
  
Or you can implement a dictionary implicitly, using "<<" and specifying the path to the dict and the separator that should be used

For example, if you have a dictionary that looks like this:

<code> hello_world_i_am_cool </code>

You should use this command:

<code> test_dict << ./path/to/dict.txt _ </code> 

so that the words will be separated using "_"

WARNING: if your dict looks like this (separated using "\n")

<code> hello </code>
  
<code>  word </code>
  
<code>  i </code>
  
<code>  am </code>
  
<code>  cool </code>

You should use this command without specifying the separator:

<code> test_dict << ./path/to/dict.txt </code>

Dicts have to be assinged to a ref as lists:

<code> !w = test_dict </code>

# How to use
Create a Brute object, specifying the settings path and the bruteforcing format

Example:

<code> b = Brute("./settings.txt", "h e l l o ?t ?t") </code>

(The bruteforce will take the single chars as static, so they won't change during the generation process)

More things that you can specify are:

Starting password (at which password he should start generating): 

<code> b = Brute(settings_path, brute_format, start = "hello11") </code>

Stopping password (at which password he should stop generating) : 

<code>  b = Brute(settings_path, brute_format, stop = "hello33") </code>

Dump options (path to the file to store the passwords in, and if it should be cleared first or not):

<code> b = Brute(settings_path,brute_format, dump = {"path" : "./dump.txt", "clear" : True}) </code>

Now the Brute object will generate a new password each time the <code>Brute.GetPassword()</code> method is called

Note that <code>Brute.GetPassword()</code> will return False if the Brute has no more passwords