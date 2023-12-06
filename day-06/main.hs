import Debug.Trace
import Control.Monad
import System.IO

--countWaysToBeat' e r = length $ filter (\t -> t * (e - t) > r) [0..e]
countWaysToBeat :: Int -> Int -> Int
countWaysToBeat e r = ceiling ((e' + q)/2) - floor ((e' - q)/2) - 1
  where
    e' = fromIntegral e
    q = sqrt . fromIntegral $ e*e - 4*r

aoc path = do
  print path
  numbers :: [[Int]] <- map (map read . drop 1 . words) . lines <$> readFile path
  guard $ length numbers == 2
  let [times, distances] = numbers
  let races = zip times distances
  let ways = flip map races $ uncurry countWaysToBeat
  print $ product ways
  let [e, r] = map (read . join . map show) numbers
  print $ countWaysToBeat e r

main = do
  forM_ ["../inputs/sample-day-06.txt", "../inputs/input-day-06.txt"] $ aoc
