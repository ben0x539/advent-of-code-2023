import Data.List
import Data.Maybe
import Data.Char
import Control.Arrow

digitWords = zip [1..] ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

digitify [] = Nothing
digitify (x:xs) | isDigit x = Just (digitToInt x)
digitify xs = fmap fst $ find ((`isPrefixOf` xs) . snd) digitWords

main = do
  input <- readFile "../inputs/input-day-01.txt"
  let digits = map (mapMaybe digitify . tails) (lines input)
  let firstAndLast = map (head &&& last) digits
  let numbers = map (\(a, b) -> a * 10 + b) firstAndLast
  print (sum numbers)
