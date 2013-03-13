module PlainWiki where

import Text.JSON
import Data.Either
import Data.Maybe
import Control.Monad

getwikijson :: IO JSValue
getwikijson = do
	raw <- readFile "../../../101dev/tools/data/generated/all.json"
	return $ head $ rights [resultToEither (decode raw)]

getField :: String -> JSValue -> Maybe JSValue
getField fieldname (JSObject object) = case dropWhile ((/= fieldname).fst) (fromJSObject object) of
	((_,h):_) -> Just h
	_		  -> Nothing

getArray :: JSValue -> [JSValue]
getArray (JSArray array) = array

getNameList :: String -> JSValue -> Maybe [String]
getNameList fieldname json = case getField fieldname json of
		Just (JSArray oobjects) -> Just $ map langstring oobjects
		Nothing 				-> Nothing
		where
			langstring object = case fromJust (getField "name" object) of
					JSString jstring -> fromJSString jstring

concatContent :: [String] -> JSValue -> String
concatContent sectionnames json = 	(concat $ map getString $ mapMaybe (\sn -> getField sn json) sectionnames) 
								 ++	(concatMap (\x -> "\n" ++ x) (fromJust (getNameList "technologies" json)))
	where
		getString (JSString jsstring) = fromJSString jsstring

main :: IO ()
main = do
	json <- getwikijson
	let impls = fromJust (getField "Implementation" json)
	let sectionnames = ["discussion", "dicussion", "architecture", "intent", "motivation", "issues", "usage", "description", "summary", "illustration"]
	forM_ (getArray impls) $ \impl -> do
		when (elem "Haskell" (fromJust (getNameList "languages" impl))) $ do
			putStrLn (concatContent sectionnames impl)	